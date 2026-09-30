# 2026-09-29: knapcio stack, reasoning effort high vs low

- `eval69_effort_high.log`: 69-scenario tool eval with the server default effort high (knapcio `.env.500k`).
  The harness sent `enable_thinking: false`, which this chat template ignores, so it ran at high.
- `eval69_effort_low.log`: the same eval after the relaunch with `DEFAULT_EFFORT=low`.
- `effort_ab.py` / `effort_ab.log`: 5 prompts, request-level `reasoning_effort` low vs high, same boot.
- `env.low`: our env file for knapcio's `start.sh` (switched fleet, 500K, effort low, fresh CTN and overlay path).
  Launch: `ENV_FILE=.env.low ./start.sh serve` from the knapcio repo on the head node.
