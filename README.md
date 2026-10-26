---
license: cc-by-4.0
pretty_name: Agent Failure Evals - Tool-Call Misuse v0.2.1
language:
- en
task_categories:
- text-classification
- text-generation
tags:
- agents
- tool-use
- evals
- coding-agents
- failure-analysis
size_categories:
- n<1K
configs:
- config_name: default
  data_files:
  - split: test
    path: data/cases.jsonl
---

# Agent Failure Evals: Tool-Call Misuse v0.2.1

## Summary
32 real-world failures where open-source **coding agents misused tool calls**. Each one comes from a public GitHub issue and is normalized into a single case with: the task, a step-level trajectory, expected vs. actual behavior, a failure category, and a gradeable pass / partial / fail rubric.

It is aimed at AI labs and agent-harness builders who want small, hand-checked regression cases for tool-calling reliability. This is an early release (v0.2.1, a correction release on top of v0.2: same 32 cases). Most trajectories are partial, and no case has been re-run against a model yet (see Caveats).

## What's in it
| Path | Contents |
|---|---|
| `data/cases.jsonl` | 32 cases, one JSON object per line (the canonical data) |
| `cases/AFE-XXXX.md` | Human-readable version of each case |
| `SHORTLIST.md` | Selection record: chosen cases, excluded cases with reasons |
| `SCORING.md` | How to grade an agent against the rubrics |
| `scripts/validate.py` | Schema and enum validator |
| `scripts/score.py` | Scores a judgments file by subtype and severity |
| `fixtures/` | Replay files for the 8 harness-confirmed cases |
| `LICENSE`, `CITATION.cff` | License and citation |

Harness repos covered: openai/codex (8), anomalyco/opencode (8), anthropics/claude-code (3), QwenLM/qwen-code (3), google-gemini/gemini-cli (2), OpenHands/OpenHands (2), aaif-goose/goose (2), and one each from continuedev/continue, cline/cline, Kilo-Org/kilocode, SWE-agent/SWE-agent.

## Schema (`data/cases.jsonl`)
| Field | Type | Description |
|---|---|---|
| case_id | string | `AFE-NNNN` |
| failure_mode | enum | `tool-call-misuse` |
| subtype | enum | `wrong-args`, `nonexistent-tool`, `ignored-error`, `wrong-channel`, `data-exfiltration`, `other` |
| severity | enum | `low`, `medium`, `high`, `critical` |
| domain | enum | `coding` (all cases) |
| agent_system | string | Harness, version, and model as reported; `not recorded` where unknown |
| harness_repo | string | `owner/repo` of the agent harness |
| source_url | string | Link to the GitHub issue |
| upstream_license | enum | License of the harness repo: `Apache-2.0`, `MIT`, `none detected` |
| case_license | string | `CC-BY-4.0`, or the paraphrase label for claude-code cases |
| repro_status | enum | See the reproduction table |
| task_input | string | The user's task and environment |
| trajectory | list | `{step, plan, tool_call, observation}`; only steps shown in the source |
| expected_behavior / actual_behavior | string | |
| failure_category | object | `{primary, secondary}` |
| rubric | object | `{pass, fail, partial}` grading criteria |
| rationale | string | Why the case matters |
| notes | string | Provenance, redactions, unverified points, reproduction details |

## Failure taxonomy (subtypes)
| Subtype | Definition | v0.2 count |
|---|---|---|
| wrong-args | The tool exists, but the arguments are malformed, of the wrong type, missing required fields, invented, or wrong for the environment | 19 |
| nonexistent-tool | The agent calls a tool name that is not advertised, either hallucinated or carried over from another harness | 8 |
| ignored-error | The tool returns an error, and the agent ignores it, repeats the call, or claims success anyway | 4 |
| wrong-channel | A tool call is emitted as plain text or markup instead of a structured call, and the agent then reports progress that did not happen | 1 |
| data-exfiltration | The agent places personal or private data from its context into an outbound tool call (a request header, URL or payload) against an instruction or without the user's consent | 0 |
| other | Anything that fits none of the subtypes above | 0 |

Added in v0.2.1: `wrong-channel` (AFE-0028 moved here from `other`) and `data-exfiltration` (no cases in this release; the first is planned for the next one). `other` stays in the schema as a catch-all and is currently empty.

## Methodology
- **Sources:** public GitHub issues on open-source coding agents, collected on 2026-10-15 (v0.1) and 2026-10-21 (v0.2) with GitHub search (several query phrasings per repo), then reading full issue bodies and comments.
- **Selection criteria (in order):**
  1. Clearly misuse by the model or agent, not a pure harness bug.
  2. A documented trajectory with real tool calls and errors.
  3. Expected vs. actual is clear enough to grade.
  4. Severity and impact.
  5. Diversity of repos and subtypes.
  6. A redistributable license.
  7. Plausibly reproducible.

  v0.1: 36 cases were drafted; 25 were selected. The other 11 are listed with reasons in `SHORTLIST.md`.
  v0.2: 20 new candidates from a weekly GitHub sweep (2026-10-21) were triaged against the same criteria; 7 were accepted (AFE-0037 to AFE-0043), 9 deferred and 4 rejected.
- **No invention:** every field comes from the issue text or logs. Unknowns are recorded as `not recorded`, and trajectories include only the steps the source shows.
- **Paraphrase policy:** the three anthropics/claude-code cases (AFE-0015, AFE-0028, AFE-0035) are entirely our own paraphrase with link-only attribution. An automated check found no run of 8 or more words copied from the source issue. The same check on the 7 v0.2 cases found only identifiers (a source file path and a short error/repro string). Other cases contain short excerpts (error strings, argument snippets), used to identify the failure, plus our own re-description.
- **Redaction:** personal paths, session and thread IDs, and similar identifiers were removed or replaced with `<redacted>`. Generic sandbox paths quoted in the issues (e.g. `/workspace/...` inside an agent container) were kept.

## Reproduction status
Nothing in v0.2 has been reproduced end-to-end with a model. "Harness-confirmed" means we ran the real harness and injected the reported bad tool call through a scripted mock model (or called the parser or tool server directly). We then confirmed the harness rejects it the way the issue describes. It does not mean the model behavior was re-observed.

| case_id | harness_repo | subtype | severity | repro_status |
|---|---|---|---|---|
| AFE-0001 | openai/codex | wrong-args | high | not attempted |
| AFE-0002 | openai/codex | wrong-args | high | not attempted |
| AFE-0003 | continuedev/continue | wrong-args | medium | not attempted |
| AFE-0004 | openai/codex | wrong-args | medium | blocked - requires Windows (PowerShell + ripgrep); not reproducible on Linux |
| AFE-0005 | cline/cline | wrong-args | medium | not attempted |
| AFE-0010 | openai/codex | nonexistent-tool | high | not attempted |
| AFE-0011 | openai/codex | ignored-error | high | blocked - requires OpenAI access to gpt-5.6-luna/terra via Codex CLI; failure is a model omission, cannot be mocked |
| AFE-0013 | openai/codex | ignored-error | medium | not attempted |
| AFE-0014 | anomalyco/opencode | wrong-args | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0015 | anthropics/claude-code | wrong-args | high | not attempted |
| AFE-0016 | anomalyco/opencode | ignored-error | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0017 | google-gemini/gemini-cli | wrong-args | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0018 | OpenHands/OpenHands | nonexistent-tool | medium | not attempted |
| AFE-0019 | OpenHands/OpenHands | nonexistent-tool | low | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0020 | aaif-goose/goose | nonexistent-tool | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0021 | anomalyco/opencode | nonexistent-tool | low | not attempted |
| AFE-0022 | QwenLM/qwen-code | nonexistent-tool | low | harness hint defect fixed upstream in v0.25.0 (QwenLM/qwen-code#12743); nonexistent-tool path confirmed on 0.25.2; model behavior not yet re-run |
| AFE-0024 | Kilo-Org/kilocode | wrong-args | high | not attempted |
| AFE-0025 | anomalyco/opencode | wrong-args | low | not attempted |
| AFE-0026 | anomalyco/opencode | wrong-args | low | not attempted |
| AFE-0027 | SWE-agent/SWE-agent | wrong-args | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0028 | anthropics/claude-code | wrong-channel | critical | not attempted |
| AFE-0033 | google-gemini/gemini-cli | wrong-args | medium | not attempted |
| AFE-0035 | anthropics/claude-code | wrong-args | medium | not attempted |
| AFE-0036 | anomalyco/opencode | wrong-args | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0037 | aaif-goose/goose | ignored-error | medium | not attempted |
| AFE-0038 | anomalyco/opencode | wrong-args | medium | not attempted |
| AFE-0039 | openai/codex | nonexistent-tool | medium | not attempted |
| AFE-0040 | QwenLM/qwen-code | wrong-args | medium | not attempted |
| AFE-0041 | QwenLM/qwen-code | wrong-args | low | not attempted |
| AFE-0042 | openai/codex | wrong-args | low | not attempted |
| AFE-0043 | anomalyco/opencode | nonexistent-tool | medium | not attempted |

Totals: 8 harness-confirmed (AFE-0022's harness hint defect is fixed upstream; its nonexistent-tool path is still confirmed), 2 blocked, 22 not attempted. The 7 cases added in v0.2 (AFE-0037 to AFE-0043) are all not attempted.

## Licensing
- **Our annotations** (normalization, trajectories as structured, rubrics, rationales, taxonomy, scripts, fixtures README) are released under **CC BY 4.0**. See `LICENSE`.
- **Upstream:** each case records its harness repo's license in `upstream_license` (Apache-2.0 for 17 cases, MIT for 12). That license covers the repository's code. It does not necessarily cover the issue text, which is posted by users under GitHub's terms. We link each source issue rather than copying it wholesale, and we quote only short identifying excerpts.
- **anthropics/claude-code** (no license detected): AFE-0015, AFE-0028 and AFE-0035 are original paraphrases, labeled `paraphrase (link-only attribution); original repo has no detected license`.
- If you are an issue author and want a case changed or removed, contact us (below) or open an issue at https://github.com/faddacake/agent-failure-evals/issues.

## Caveats and limitations
- **Partial trajectories:** most cases show only the steps quoted in the issue. Several are a single step, or are aggregated by the reporter (e.g. "15 calls failed").
- **No model reruns:** no case has been re-observed with the reported model. Harness-confirmed cases only verify the error path.
- **Version drift:** some harness-confirmed results used newer harness versions than the reports. Error wording differs for AFE-0019 and AFE-0020, and the bad suggestion hint reported in AFE-0022 was fixed upstream in Qwen Code v0.25.0 (QwenLM/qwen-code#12743); results recorded against v0.24.5 or earlier describe the pre-fix harness. Details are in each case's notes.
- **Skew:** openai/codex and anomalyco/opencode account for 16 of 32 cases. ignored-error (4) and wrong-channel (1) are underrepresented, and data-exfiltration has no cases yet.
- **Harness-vs-model ambiguity:** in some cases (e.g. AFE-0003, AFE-0022, AFE-0024, AFE-0042, AFE-0043) the harness contributes to the failure. Cases where the harness clearly dominated were excluded.
- **Severity** is our judgment, not the reporter's.
- **Small size (32):** this set is for regression testing and qualitative evaluation, not statistically powered benchmarking.

## Intended use
- Regression tests for agent harnesses: tool-schema validation, unknown-tool handling, retry and loop guards, error propagation.
- Qualitative evaluation of whether a model or agent recovers from tool errors, scored with the per-case rubrics (see `SCORING.md`).
- Seed examples for building larger synthetic or reproduced failure suites.

Not intended to rank models on its own, or as evidence about any specific vendor beyond the reported incidents.

## Citation
```bibtex
@misc{agent_failure_evals_tcm_v021,
  title  = {Agent Failure Evals: Tool-Call Misuse v0.2.1},
  author = {Harrelson, Ben},
  year   = {2026},
  note   = {32 real-world tool-call misuse cases from open-source coding agents},
  howpublished = {\url{https://github.com/faddacake/agent-failure-evals}}
}
```

## Contact
GitHub: [@faddacake](https://github.com/faddacake) (also open an issue on the dataset repo for change/removal requests: https://github.com/faddacake/agent-failure-evals/issues)

## Changelog
- **v0.2.1 (2026-10-26):** correction and taxonomy release; no new cases (32 cases, same as v0.2). Adds the `wrong-channel` and `data-exfiltration` subtypes to the schema and taxonomy; AFE-0028 moves from `other` to `wrong-channel`. Corrects AFE-0022: the harness hint defect was fixed upstream in Qwen Code v0.25.0 (QwenLM/qwen-code#12743), so the case now grades only the model's recovery; flagged by Qwen Code triage. Counts: 19 wrong-args, 8 nonexistent-tool, 4 ignored-error, 1 wrong-channel, 0 data-exfiltration, 0 other. `scripts/validate.py` accepts the new subtypes and the updated AFE-0022 repro label.
- **v0.2 (2026-10-21):** adds 7 cases (AFE-0037 to AFE-0043) from a 2026-10-21 sweep of public issues: goose no-op edit reported as success, opencode fabricated subagent `sessionID` and `tools.read` inside Code Mode `execute`, Codex tool call emitted as a compaction summary and `list_threads` limit above an undocumented cap, Qwen Code `tool_call` envelope nested one level too deep and deferred `get_goal` called before schema review. Now 32 cases (19 wrong-args, 8 nonexistent-tool, 4 ignored-error, 1 other). New cases are not attempted for reproduction; fixtures unchanged.
- **v0.1 (2026-10-15):** first release candidate. 25 cases (15 wrong-args, 6 nonexistent-tool, 3 ignored-error, 1 other); 8 harness-confirmed with replay fixtures.
