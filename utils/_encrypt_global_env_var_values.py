from typing import Any, Dict

def _encrypt_global_env_var_values(env_vars: Iterable[Dict[str, Any]]) -> None:
    """Encrypt ``scope="global"`` env var values in place before persisting.

    Global values hold admin-supplied secrets (API keys, passwords) that get
    interpolated into headers, so they are encrypted at rest like credentials
    and the per-user ``values_b64`` column. Per-user placeholders are not
    secrets and are stored verbatim.
    """
    for entry in env_vars:
        if not _is_global_env_var_scope(entry.get("scope")):
            continue
        value = entry.get("value")
        if value:
            entry["value"] = encrypt_value_helper(value)

