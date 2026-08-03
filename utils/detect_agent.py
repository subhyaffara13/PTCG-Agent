import os
from typing import Optional

def detect_agent() -> Optional[str]:
    """Return the id of the detected AI agent harness or `None`.

    Harnesses are checked in registry order; for each one we match its env var
    pattern(s) and, failing that, the standard `AI_AGENT` / `AGENT` vars
    against the harness id. The first match wins. When a standard var is set to
    an unrecognized value, `"unknown"` is returned.
    """
    registry = _get_registry()
    standard_vars = registry.get("standardEnvVars") or []
    harnesses = registry.get("harnesses") or {}

    for harness_id, info in harnesses.items():
        env_vars = (info or {}).get("envVars")
        if env_vars and _env_vars_match(env_vars):
            return harness_id
        for var in standard_vars:
            if os.environ.get(var, "").strip() == harness_id:
                return harness_id

    # No harness matched but a standard var is set => unrecognized agent.
    lowercased_harnesses = {k.lower() for k in harnesses.keys()}
    for var in standard_vars:
        if value := os.environ.get(var, "").strip().lower():
            if value in lowercased_harnesses:
                return value
            return "unknown"

    return None

