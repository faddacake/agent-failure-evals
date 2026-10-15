---
license: cc-by-4.0
pretty_name: Agent Failure Evals - Tool-Call Misuse v0.1
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

# Agent Failure Evals: Tool-Call Misuse v0.1

## Summary
25 real-world failures where open-source **coding agents misused tool calls**. Each one comes from a public GitHub issue and is normalized into a single case with: the task, a step-level trajectory, expected vs. actual behavior, a failure category, and a gradeable pass / partial / fail rubric.

It is aimed at AI labs and agent-harness builders who want small, hand-checked regression cases for tool-calling reliability. This is an early release (v0.1). Most trajectories are partial, and no case has been re-run against a model yet (see Caveats).

## What's in it
| Path | Contents |
|---|---|
| `data/cases.jsonl` | 25 cases, one JSON object per line (the canonical data) |
| `cases/AFE-XXXX.md` | Human-readable version of each case |
| `SHORTLIST.md` | Selection record: chosen cases, excluded cases with reasons |
| `SCORING.md` | How to grade an agent against the rubrics |
| `scripts/validate.py` | Schema and enum validator |
| `scripts/score.py` | Scores a judgments file by subtype and severity |
| `fixtures/` | Replay files for the 8 harness-confirmed cases |
| `LICENSE`, `CITATION.cff` | License and citation |

Harness repos covered: openai/codex (6), anomalyco/opencode (6), anthropics/claude-code (3), google-gemini/gemini-cli (2), OpenHands/OpenHands (2), and one each from continuedev/continue, cline/cline, aaif-goose/goose, QwenLM/qwen-code, Kilo-Org/kilocode, SWE-agent/SWE-agent.

## Schema (`data/cases.jsonl`)
| Field | Type | Description |
|---|---|---|
| case_id | string | `AFE-NNNN` |
| failure_mode | enum | `tool-call-misuse` |
| subtype | enum | `wrong-args`, `nonexistent-tool`, `ignored-error`, `other` |
| severity | enum | `low`, `medium`, `high`, `critical` |
| domain | enum | `coding` (all v0.1 cases) |
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
| Subtype | Definition | v0.1 count |
|---|---|---|
| wrong-args | The tool exists, but the arguments are malformed, of the wrong type, missing required fields, invented, or wrong for the environment | 15 |
| nonexistent-tool | The agent calls a tool name that is not advertised, either hallucinated or carried over from another harness | 6 |
| ignored-error | The tool returns an error, and the agent ignores it, repeats the call, or claims success anyway | 3 |
| other | A tool call is emitted in the wrong channel (as text, not a structured call), and the agent then reports progress that didn't happen | 1 |

## Methodology
- **Sources:** public GitHub issues on open-source coding agents, collected on 2026-10-15 with GitHub search (several query phrasings per repo), then reading full issue bodies and comments.
- **Selection criteria (in order):**
  1. Clearly misuse by the model or agent, not a pure harness bug.
  2. A documented trajectory with real tool calls and errors.
  3. Expected vs. actual is clear enough to grade.
  4. Severity and impact.
  5. Diversity of repos and subtypes.
  6. A redistributable license.
  7. Plausibly reproducible.

  36 cases were drafted; 25 were selected. The other 11 are listed with reasons in `SHORTLIST.md`.
- **No invention:** every field comes from the issue text or logs. Unknowns are recorded as `not recorded`, and trajectories include only the steps the source shows.
- **Paraphrase policy:** the three anthropics/claude-code cases (AFE-0015, AFE-0028, AFE-0035) are entirely our own paraphrase with link-only attribution. An automated check found no run of 8 or more words copied from the source issue. Other cases contain short excerpts (error strings, argument snippets), used to identify the failure, plus our own re-description.
- **Redaction:** personal paths, session and thread IDs, and similar identifiers were removed or replaced with `<redacted>`. Generic sandbox paths quoted in the issues (e.g. `/workspace/...` inside an agent container) were kept.

## Reproduction status
Nothing in v0.1 has been reproduced end-to-end with a model. "Harness-confirmed" means we ran the real harness and injected the reported bad tool call through a scripted mock model (or called the parser or tool server directly). We then confirmed the harness rejects it the way the issue describes. It does not mean the model behavior was re-observed.

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
| AFE-0022 | QwenLM/qwen-code | nonexistent-tool | low | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0024 | Kilo-Org/kilocode | wrong-args | high | not attempted |
| AFE-0025 | anomalyco/opencode | wrong-args | low | not attempted |
| AFE-0026 | anomalyco/opencode | wrong-args | low | not attempted |
| AFE-0027 | SWE-agent/SWE-agent | wrong-args | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |
| AFE-0028 | anthropics/claude-code | other | critical | not attempted |
| AFE-0033 | google-gemini/gemini-cli | wrong-args | medium | not attempted |
| AFE-0035 | anthropics/claude-code | wrong-args | medium | not attempted |
| AFE-0036 | anomalyco/opencode | wrong-args | medium | harness-confirmed (bad call injected; model behavior not yet re-run) |

Totals: 8 harness-confirmed, 2 blocked, 15 not attempted.

## Licensing
- **Our annotations** (normalization, trajectories as structured, rubrics, rationales, taxonomy, scripts, fixtures README) are released under **CC BY 4.0**. See `LICENSE`.
- **Upstream:** each case records its harness repo's license in `upstream_license` (Apache-2.0 for 12 cases, MIT for 10). That license covers the repository's code. It does not necessarily cover the issue text, which is posted by users under GitHub's terms. We link each source issue rather than copying it wholesale, and we quote only short identifying excerpts.
- **anthropics/claude-code** (no license detected): AFE-0015, AFE-0028 and AFE-0035 are original paraphrases, labeled `paraphrase (link-only attribution); original repo has no detected license`.
- If you are an issue author and want a case changed or removed, contact us (below) or open an issue at https://github.com/faddacake/agent-failure-evals/issues.

## Caveats and limitations
- **Partial trajectories:** most cases show only the steps quoted in the issue. Several are a single step, or are aggregated by the reporter (e.g. "15 calls failed").
- **No model reruns:** no case has been re-observed with the reported model. Harness-confirmed cases only verify the error path.
- **Version drift:** some harness-confirmed results used newer harness versions than the reports. Error wording differs for AFE-0019 and AFE-0020, and the bad suggestion hint reported in AFE-0022 is fixed in Qwen Code 0.25.2. Details are in each case's notes.
- **Skew:** openai/codex and anomalyco/opencode account for 12 of 25 cases. ignored-error (3) and other (1) are underrepresented.
- **Harness-vs-model ambiguity:** in some cases (e.g. AFE-0003, AFE-0022, AFE-0024) the harness contributes to the failure. Cases where the harness clearly dominated were excluded.
- **Severity** is our judgment, not the reporter's.
- **Small size (25):** this set is for regression testing and qualitative evaluation, not statistically powered benchmarking.

## Intended use
- Regression tests for agent harnesses: tool-schema validation, unknown-tool handling, retry and loop guards, error propagation.
- Qualitative evaluation of whether a model or agent recovers from tool errors, scored with the per-case rubrics (see `SCORING.md`).
- Seed examples for building larger synthetic or reproduced failure suites.

Not intended to rank models on its own, or as evidence about any specific vendor beyond the reported incidents.

## Citation
```bibtex
@misc{agent_failure_evals_tcm_v01,
  title  = {Agent Failure Evals: Tool-Call Misuse v0.1},
  author = {Harrelson, Ben},
  year   = {2026},
  note   = {25 real-world tool-call misuse cases from open-source coding agents},
  howpublished = {\url{https://github.com/faddacake/agent-failure-evals}}
}
```

## Contact
GitHub: [@faddacake](https://github.com/faddacake) (also open an issue on the dataset repo for change/removal requests: https://github.com/faddacake/agent-failure-evals/issues)

## Changelog
- **v0.1 (2026-10-15):** first release candidate. 25 cases (15 wrong-args, 6 nonexistent-tool, 3 ignored-error, 1 other); 8 harness-confirmed with replay fixtures. Prepared, not yet published.
