
def decrypt_global_env_var_values(env_vars: Optional[Iterable[Any]]) -> None:
    """Decrypt ``scope="global"`` env var values in place after reading the DB.

    Accepts ``MCPEnvVar`` models (``LiteLLM_MCPServerTable``) or plain dicts
    (raw rows / deserialized JSON). Global values are always stored encrypted,
    so a value that no longer decrypts (e.g. after a salt-key change) is dropped
    and a warning is logged rather than forwarding the ciphertext into upstream
    ``${NAME}`` headers, where it would silently fail.
    """
    if not env_vars:
        return
    for entry in env_vars:
        is_dict = isinstance(entry, dict)
        scope = entry.get("scope") if is_dict else getattr(entry, "scope", None)
        if not _is_global_env_var_scope(scope):
            continue
        value = entry.get("value") if is_dict else getattr(entry, "value", None)
        if not value:
            continue
        decrypted = decrypt_value_helper(
            value=value,
            key="mcp_global_env_var",
            exception_type="debug",
            return_original_value=False,
        )
        if decrypted is None:
            name = entry.get("name") if is_dict else getattr(entry, "name", None)
            verbose_proxy_logger.warning(
                "MCP global env var %s failed to decrypt (LITELLM_SALT_KEY "
                "changed?); dropping it so ciphertext is not sent upstream",
                name,
            )
            decrypted = ""
        if is_dict:
            entry["value"] = decrypted
        else:
            entry.value = decrypted

