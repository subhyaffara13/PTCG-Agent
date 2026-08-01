
def _reencrypt_global_env_var_values(
    env_vars: Optional[Iterable[Any]], new_encryption_key: str
) -> Optional[List[Dict[str, Any]]]:
    """Re-encrypt ``scope="global"`` env var values for master-key rotation.

    Each global value is decrypted with the current salt key and re-encrypted
    under ``new_encryption_key``. Returns the rebuilt list when at least one
    value was rotated, else ``None`` so the caller can skip the DB write. A
    value that fails to decrypt is left untouched (and logged) so a corrupt
    entry is preserved for recovery rather than overwritten.
    """
    if not env_vars:
        return None
    if isinstance(env_vars, str):
        try:
            env_vars = json.loads(env_vars)
        except (json.JSONDecodeError, TypeError):
            return None
        if not env_vars:
            return None
    rebuilt = [dict(v) for v in env_vars]
    rotated = False
    for entry in rebuilt:
        if not _is_global_env_var_scope(entry.get("scope")):
            continue
        value = entry.get("value")
        if not value:
            continue
        decrypted = decrypt_value_helper(
            value=value,
            key="mcp_global_env_var",
            exception_type="debug",
            return_original_value=False,
        )
        if decrypted is None:
            verbose_proxy_logger.warning(
                "rotate_mcp_server_credentials_master_key: could not decrypt "
                "global env var %s, skipping",
                entry.get("name"),
            )
            continue
        entry["value"] = encrypt_value_helper(
            decrypted, new_encryption_key=new_encryption_key
        )
        rotated = True
    return rebuilt if rotated else None

