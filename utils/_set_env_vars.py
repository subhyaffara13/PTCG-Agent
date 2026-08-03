import os
from typing import Any, Dict

def _set_env_vars(config_data: Dict[str, Any]) -> None:
    """Set HCP_VAULT_* env vars from config data. Unsets vars for missing/None/empty fields."""
    for field_name, env_var_name in HASHICORP_ENV_VAR_MAPPING.items():
        value = config_data.get(field_name)
        if value is not None and value != "":
            os.environ[env_var_name] = str(value)
        else:
            os.environ.pop(env_var_name, None)

