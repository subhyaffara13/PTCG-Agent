
def _redact_record_env_vars(record: Any) -> Any:
    """Return ``record`` with its ``env_vars[].value`` blanked.

    Copies rather than mutating, because the record aliases the live response
    object that is also returned to the caller. Records without an ``env_vars``
    list are returned unchanged.
    """
    env_vars = (
        record.get("env_vars")
        if isinstance(record, dict)
        else getattr(record, "env_vars", None)
    )
    if not isinstance(env_vars, list):
        return record
    redacted = [_redacted_env_var(entry) for entry in env_vars]
    if isinstance(record, dict):
        return {**record, "env_vars": redacted}
    if isinstance(record, BaseModel):
        return record.model_copy(update={"env_vars": redacted})
    return record

