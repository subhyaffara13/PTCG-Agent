from typing import Any

def _redacted_env_var(entry: Any) -> dict:
    get = entry.get if isinstance(entry, dict) else lambda k: getattr(entry, k, None)
    return {
        "name": get("name"),
        "scope": get("scope"),
        "description": get("description"),
        "value": "",
    }

