from typing import Any, Optional

def _resolve_secret(value: Any) -> Optional[str]:
    """Resolve a config value, expanding ``os.environ/`` references."""
    if not isinstance(value, str):
        return None
    if value.startswith("os.environ/"):
        return get_secret_str(value)
    return value

