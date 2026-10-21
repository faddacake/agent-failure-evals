# v0.1 Shortlist (selection record)

_Cleaned copy of the internal shortlist. Wikilinks are converted to plain IDs. Repro statuses here use the internal wording; data/cases.jsonl carries the release labels._


**Purpose:** Pick the ~25 strongest of the 36 tool-call-misuse cases for the first open dataset (v0.1) aimed at labs and vertical harness builders.

**Next action:** Reproduce the 10 `repro-priority` cases in a sandbox.

**Definition of done:** Every selected case is license-cleared (or re-described with link only), has a gradeable rubric, and at least 10 are reproduced.

## Selection criteria (in order)
1. Clearly a model/agent tool-call misuse, not a pure harness bug
2. Documented trajectory with real tool calls and errors
3. Clear expected vs actual, so the rubric can be graded
4. Severity / impact
5. Repo diversity and subtype balance
6. Redistributable license
7. Plausibly reproducible

## Selected (25)

| case_id | repo | subtype | severity | license | reason | caveats | repro-priority |
|---|---|---|---|---|---|---|---|
| AFE-0001 | openai/codex | wrong-args | high | Apache-2.0 | Verbatim rollout lines: exec_command args `"{"` → parse error | custom vLLM model; 2 steps only | n |
| AFE-0002 | openai/codex | wrong-args | high | Apache-2.0 | Shell command array sent as JSON string; all shell use blocked | error strings only, order not recorded | n |
| AFE-0003 | continuedev/continue | wrong-args | medium | Apache-2.0 | Array params sent as strings on every call after the first | possibly harness re-serialization (unverified commenter hypothesis) | n |
| AFE-0004 | openai/codex | wrong-args | medium | Apache-2.0 | Bash-style rg glob repeated under PowerShell despite os error 123 | repetition described, not logged; Windows-only | y; repro: no |
| AFE-0005 | cline/cline | wrong-args | medium | Apache-2.0 | Large edit payload → unterminated JSON; session hang | single step; path redacted | n |
| AFE-0010 | openai/codex | nonexistent-tool | high | Apache-2.0 | Reviewer claims a `make_pr` call and SHAs that don't exist | final comment only, no trajectory; private repo | n |
| AFE-0011 | openai/codex | ignored-error | high | Apache-2.0 | Skips image_gen, replies DONE rc=0; model-controlled comparison | model versions may be retired | y; repro: no |
| AFE-0013 | openai/codex | ignored-error | medium | Apache-2.0 | Invented skill path, rationalized ENOENT, bypassed mandatory read | model not recorded | n |
| AFE-0014 | anomalyco/opencode | wrong-args | medium | MIT | 5+ read calls with string offset; reasoning shown at each step | new session did not reproduce for reporter | y; repro: partial (harness-level) |
| AFE-0015 | anthropics/claude-code | wrong-args | high | paraphrase (link-only) | Monitor: placeholder `ws` on all 15 calls; ignores acknowledged fix | call ordering aggregated | n |
| AFE-0016 | anomalyco/opencode | ignored-error | medium | MIT | Hallucinated oldString repeated 10+ times after not-found error | steps described, not raw log | y; repro: partial (harness-level) |
| AFE-0017 | google-gemini/gemini-cli | wrong-args | medium | Apache-2.0 | MCP param def1 vs def, repeated after error and user correction | exact args not shown | y; repro: partial (harness-level) |
| AFE-0018 | OpenHands/OpenHands | nonexistent-tool | medium | MIT | Sonnet calls nonexistent execute_python, quoted args | single step | n |
| AFE-0019 | OpenHands/OpenHands | nonexistent-tool | low | MIT | devstral calls execute_code; error lists valid tools | single step; recovery not recorded | y; repro: partial (harness-level) |
| AFE-0020 | aaif-goose/goose | nonexistent-tool | medium | Apache-2.0 | Cross-harness names (read_file, run_command) despite tools array | order/args not recorded; fixed upstream | y; repro: partial (harness-level) |
| AFE-0021 | anomalyco/opencode | nonexistent-tool | low | MIT | Qwen3 Coder calls another harness's todo_write | thin: one error line | n |
| AFE-0022 | QwenLM/qwen-code | nonexistent-tool | low | Apache-2.0 | edit_file_path with empty args, ~6x/session | harness hint co-cause; model not recorded | y; repro: partial (harness-level) |
| AFE-0024 | Kilo-Org/kilocode | wrong-args | high | MIT | Subagent loops on empty edit; ignores 3 corrective prompts | model not recorded; partly harness (no stop) | n |
| AFE-0025 | anomalyco/opencode | wrong-args | low | MIT | shell called with `cmd` instead of `command` | single step; log attachment not reviewed | n |
| AFE-0026 | anomalyco/opencode | wrong-args | low | MIT | Sonnet 4.6 omits nested required `question` field | single call | n |
| AFE-0027 | SWE-agent/SWE-agent | wrong-args | medium | MIT | deepseek-r1 emits JSON call where thought_action expected | public tutorial task | y; repro: partial (harness-level) |
| AFE-0028 | anthropics/claude-code | other | critical | paraphrase (link-only) | 23 Bash calls emitted as text; git/PR actions narrated as done | commands not quoted | n |
| AFE-0033 | google-gemini/gemini-cli | wrong-args | medium | Apache-2.0 | write_file without file_path after user steering | single step; attachment not reviewed | n |
| AFE-0035 | anthropics/claude-code | wrong-args | medium | paraphrase (link-only) | 10 consecutive empty Write calls on a large-content write | dup of #895 | n |
| AFE-0036 | anomalyco/opencode | wrong-args | medium | MIT | Gemma 4 broken herestring syntax retried in loop | described with example, not raw log | y; repro: partial (harness-level) |

## License hold: resolved by paraphrase (2026-10-15)
AFE-0015, AFE-0028 and AFE-0035 were rewritten as original paraphrases with link-only attribution (`rewrite: paraphrased-2026-10-15`). An automated check found no 8-word run copied verbatim from the issues.
AFE-0029 and AFE-0031 remain excluded for the reasons listed below; their license status was not changed.

## Excluded / later (11)

| case_id | repo | reason |
|---|---|---|
| AFE-0006 | openai/codex | Harness-leaning: synthetic mock-provider call; the defect is re-execution by the harness |
| AFE-0007 | openai/codex | Harness-leaning (history replay); not reproduced; tool name not recorded |
| AFE-0008 | openai/codex | Corrupted name (NUL bytes); cause unclear (model vs persistence) |
| AFE-0009 | cline/cline | Thin (status: thin); illustrative example only |
| AFE-0012 | google-gemini/gemini-cli | Harness-leaning: status masking; main agent did notice the failure |
| AFE-0023 | Kilo-Org/kilocode | Harness crash dominates; thin single example |
| AFE-0029 | anthropics/claude-code | Zero-tool-call fabrication, not misuse of a call; fragments only; license hold. Later: fabricated-completion set |
| AFE-0030 | anomalyco/opencode | Harness-leaning: masking of a provider MALFORMED_FUNCTION_CALL |
| AFE-0031 | anthropics/claude-code | Harness accounting of API errors; no model misuse; license hold |
| AFE-0032 | cline/cline | Harness exit-code masking dominates; model error minor |
| AFE-0034 | cline/cline | Model-vs-server-vs-harness attribution unresolved |

## Repro-priority (10)
Repro pass 2026-10-15: 0 yes, 8 partial (harness-level), 2 no (AFE-0004 needs Windows; AFE-0011 needs gpt-5.6 access). Details are in each case's Reproduction section.
AFE-0004, AFE-0011, AFE-0014, AFE-0016, AFE-0017, AFE-0019, AFE-0020, AFE-0022, AFE-0027, AFE-0036

## Summary
- **Selected:** 25 cases. **Excluded / later:** 11.
- **By repo:** openai/codex 6, anomalyco/opencode 6, anthropics/claude-code 3, google-gemini/gemini-cli 2, OpenHands 2, continue 1, cline 1, goose 1, qwen-code 1, kilocode 1, SWE-agent 1.
- **By subtype:** wrong-args 15, nonexistent-tool 6, ignored-error 3, other 1. Ignored-error is underweight; source more of it in pass 3.
- **By license:** Apache-2.0 12, MIT 10, paraphrase (link-only) 3, hold 0.

## v0.2 additions (2026-10-21)
Triaged from the 2026-10-21 weekly sweep (20 candidates: 7 accepted, 9 deferred, 4 rejected) against the same criteria, then approved for v0.2.

| case_id | repo | subtype | severity | license | reason | caveats | repro-priority |
|---|---|---|---|---|---|---|---|
| AFE-0037 | aaif-goose/goose | ignored-error | medium | Apache-2.0 | No-op `edit` reported as success; model repeats it | repeat count not recorded; harness co-cause | y; repro: not attempted |
| AFE-0038 | anomalyco/opencode | wrong-args | medium | MIT | Optional subagent `sessionID` filled with invented IDs; retried after not-found | model and retry count not recorded | y; repro: not attempted |
| AFE-0039 | openai/codex | nonexistent-tool | medium | Apache-2.0 | Tool call emitted as compaction summary with no tools offered (20 of 119) | aggregate trace; model-specific | y; repro: not attempted |
| AFE-0040 | QwenLM/qwen-code | wrong-args | medium | Apache-2.0 | `tool_call` envelope nested one level too deep; error misread, tool abandoned | no full transcript | y; repro: not attempted |
| AFE-0041 | QwenLM/qwen-code | wrong-args | low | Apache-2.0 | Deferred `get_goal` called before schema review; one refusal, clean recovery | partial-band calibration case | n |
| AFE-0042 | openai/codex | wrong-args | low | Apache-2.0 | `list_threads` limit above undocumented cap; recovers in one step | borderline scope (schema gap) | n |
| AFE-0043 | anomalyco/opencode | nonexistent-tool | medium | MIT | Built-in `read` called as `tools.read` inside `execute`; several wasted turns | prompt wording co-cause; model not named | n |
