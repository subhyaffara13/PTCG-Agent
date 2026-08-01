
def _decrypt_env_vars_on_returned_row(row: Any) -> None:
    """Decrypt ``scope="global"`` env var values on a row returned by Prisma create/update.

    Prisma may hand back ``env_vars`` either as a parsed list (the common case for
    JSONB columns) or as a raw JSON string (observed for some write paths). The
    in-place decrypt helper only mutates iterables of dicts/models, so a string
    payload would silently skip decryption and ciphertext would leak into the
    registry via ``add_server``/``update_server`` (which trust the caller).
    Parse the string back to a list so the in-place decrypt actually runs, and
    write the decrypted list back onto the row so downstream consumers see plain
    values.
    """
    env_vars = getattr(row, "env_vars", None)
    if env_vars is None:
        return
    if isinstance(env_vars, str):
        try:
            env_vars = json.loads(env_vars)
        except (json.JSONDecodeError, TypeError):
            return
        if not isinstance(env_vars, list):
            return
        try:
            setattr(row, "env_vars", env_vars)
        except (AttributeError, TypeError):
            pass
    decrypt_global_env_var_values(env_vars)

