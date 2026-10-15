# Fixtures (harness-confirmed cases)

These were recorded on 2026-10-15 on Debian 13 x86_64, with no model and no API keys. Each one injects the bad tool call reported in the source issue, and records how the real harness handled it. Box-specific paths are replaced with `<sandbox>`.

| Case | Harness (version) | Method | Files |
|---|---|---|---|
| AFE-0014 | opencode 1.19.1 | `mock.py` replays `read` with a string `offset` | injected_responses.json, harness_replay.json, run.log |
| AFE-0016 | opencode 1.19.1 | `mock.py` replays `read`, then an `edit` with a non-matching oldString, 3 times | same |
| AFE-0020 | goose 1.54.0 | `mock.py` replays the unadvertised `read_file`, `view_file`, `run_command` | same |
| AFE-0022 | Qwen Code 0.25.2 | `mock.py` replays `edit_file_path` with empty args, twice | same |
| AFE-0036 | opencode 1.19.1, zsh 5.9 | `mock.py` replays a bash command with a broken `<<<` herestring, twice | same |
| AFE-0017 | pokemon-gen3-calc-mcp @ ea26f8f | stdio JSON-RPC client calls `calculate_status` with `def1` (3x), then a control call with `def` | client.py, run.log |
| AFE-0019 | openhands-ai 0.39.0 | Feeds a `execute_code` tool call to `response_to_actions` | repro.py, run.log |
| AFE-0027 | SWE-agent 1.1.0 | ThoughtActionParser on a JSON action, then run in bash | repro.py, run.log |

## mock.py
`python fixtures/mock.py PORT injected_responses.json LOGDIR` starts a minimal OpenAI-compatible `/v1/chat/completions` server (streaming and non-streaming). It returns the scripted responses in order and logs every request.

Some harnesses make a title or summary request first. That request uses up the first scripted entry, so the opencode fixtures start with a `{"text":"title"}` placeholder. In goose, it used up the first `read_file` entry.

Notes:
- `harness_replay.json` keeps only the assistant and tool messages from the last request; system prompts are omitted.
- Error wording can differ from the original reports, because newer harness versions were used. Each case's notes say where.
