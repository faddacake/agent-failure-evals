#!/usr/bin/env python3
"""Validate data/cases.jsonl: required fields, types, allowed enums. Exit 1 on any error."""
import json, sys, pathlib
P = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).parent.parent / "data/cases.jsonl")
REQ = ["case_id","failure_mode","subtype","severity","domain","agent_system","harness_repo","source_url","upstream_license",
       "case_license","repro_status","task_input","trajectory","expected_behavior","actual_behavior","failure_category",
       "rubric","rationale","notes"]
ENUM = {"failure_mode": {"tool-call-misuse"},
        "subtype": {"wrong-args","nonexistent-tool","ignored-error","other"},
        "severity": {"low","medium","high","critical"},
        "domain": {"coding","browser","support","other"},
        "upstream_license": {"Apache-2.0","MIT","none detected"}}
REPRO = {"harness-confirmed (bad call injected; model behavior not yet re-run)",
         "blocked - requires Windows (PowerShell + ripgrep); not reproducible on Linux",
         "blocked - requires OpenAI access to gpt-5.6-luna/terra via Codex CLI; failure is a model omission, cannot be mocked",
         "not attempted"}
CASELIC = {"CC-BY-4.0","paraphrase (link-only attribution); original repo has no detected license"}
errs, ids = [], set()
for ln, line in enumerate(P.read_text().splitlines(), 1):
    if not line.strip(): continue
    try: r = json.loads(line)
    except Exception as e: errs.append(f"line {ln}: invalid JSON ({e})"); continue
    cid = r.get("case_id", f"line{ln}")
    for k in REQ:
        if k not in r: errs.append(f"{cid}: missing {k}")
    for k, allowed in ENUM.items():
        if k in r and r[k] not in allowed: errs.append(f"{cid}: {k}={r[k]!r} not in {sorted(allowed)}")
    if r.get("repro_status") not in REPRO: errs.append(f"{cid}: bad repro_status")
    if r.get("case_license") not in CASELIC: errs.append(f"{cid}: bad case_license")
    if not str(r.get("source_url","")).startswith("https://github.com/"): errs.append(f"{cid}: source_url not a GitHub URL")
    t = r.get("trajectory")
    if not isinstance(t, list) or not t: errs.append(f"{cid}: trajectory must be a non-empty list")
    else:
        for i, s in enumerate(t):
            if set(s) != {"step","plan","tool_call","observation"}: errs.append(f"{cid}: trajectory[{i}] keys {sorted(s)}")
    if set(r.get("failure_category", {})) != {"primary","secondary"}: errs.append(f"{cid}: failure_category keys")
    if set(r.get("rubric", {})) != {"pass","fail","partial"}: errs.append(f"{cid}: rubric keys")
    elif not r["rubric"]["pass"] or not r["rubric"]["fail"]: errs.append(f"{cid}: rubric pass/fail empty")
    if cid in ids: errs.append(f"{cid}: duplicate case_id")
    ids.add(cid)
print(f"checked {len(ids)} cases from {P}")
if errs:
    print("\n".join("ERROR " + e for e in errs)); sys.exit(1)
print("OK: all cases valid")
