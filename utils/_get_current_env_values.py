import os
from typing import Any, Dict

def _get_current_env_values(env_var_mapping: Dict[str, str]) -> Dict[str, Any]:
    """Read current env var values as fallback when no DB record exists."""
    values = {}
    for field_name, env_var_name in env_var_mapping.items():
        env_value = os.environ.get(env_var_name)
        values[field_name] = env_value
    return values

