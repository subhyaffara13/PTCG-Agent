import os

def _env_vars_match(env_vars: dict[str, str]) -> bool:
    """Return `True` if any `(var, pattern)` from the harness matches the environment.

    Supported patterns:
      - `"*"`: the variable is set to any non-empty value
      - `"<value>"`: the variable equals this exact value
    """
    for var, pattern in env_vars.items():
        value = os.environ.get(var)
        if not value:
            continue
        if pattern == "*":
            return True
        if value == pattern:
            return True
    return False

