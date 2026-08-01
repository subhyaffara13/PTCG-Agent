
def _clear_hashicorp_vault_state(proxy_config: Any) -> None:
    """Clear all Hashicorp Vault state: env vars, secret manager, and change-detection cache."""
    _set_env_vars({})
    if litellm._key_management_system == KeyManagementSystem.HASHICORP_VAULT:
        litellm.secret_manager_client = None
        litellm._key_management_system = None
    proxy_config._last_hashicorp_vault_config = None

