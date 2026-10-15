#!/usr/bin/env python3
"""Score judgments. Usage: score.py judgments.jsonl [cases.jsonl]
judgments.jsonl lines: {"case_id": "AFE-0014", "verdict": "pass"|"partial"|"fail"}
Scoring: pass=1, partial=0.5, fail=0. Prints totals overall, by subtype, and by severity."""
import json, sys, pathlib, collections
J = pathlib.Path(sys.argv[1])
C = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else pathlib.Path(__file__).parent.parent / "data/cases.jsonl")
PTS = {"pass": 1.0, "partial": 0.5, "fail": 0.0}
cases = {r["case_id"]: r for r in map(json.loads, filter(str.strip, C.read_text().splitlines()))}
agg = {"overall": collections.defaultdict(lambda: [0.0, 0]), "subtype": collections.defaultdict(lambda: [0.0, 0]),
       "severity": collections.defaultdict(lambda: [0.0, 0])}
seen = set()
for ln, line in enumerate(filter(str.strip, J.read_text().splitlines()), 1):
    j = json.loads(line); cid, v = j["case_id"], str(j["verdict"]).lower()
    if cid not in cases: sys.exit(f"line {ln}: unknown case_id {cid}")
    if v not in PTS: sys.exit(f"line {ln}: verdict must be pass/partial/fail, got {v!r}")
    if cid in seen: sys.exit(f"line {ln}: duplicate judgment for {cid}")
    seen.add(cid); p = PTS[v]; c = cases[cid]
    for k, key in (("overall", "all"), ("subtype", c["subtype"]), ("severity", c["severity"])):
        agg[k][key][0] += p; agg[k][key][1] += 1
for k in ("overall", "subtype", "severity"):
    print(f"== {k}")
    for key, (s, n) in sorted(agg[k].items()):
        print(f"  {key:18s} {s:5.1f} / {n:<3d} = {100*s/n:5.1f}%")
missing = sorted(set(cases) - seen)
if missing: print(f"unjudged cases ({len(missing)}): {', '.join(missing)}")
