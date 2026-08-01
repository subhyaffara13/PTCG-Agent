
def _log_budget_lookup_failure(entity: str, error: Exception) -> None:
    """
    Log a warning when budget lookup fails; cache will not be populated.

    Skips logging for expected "user not found" cases (bare Exception from
    get_user_object when user_id_upsert=False). Adds a schema migration hint
    when the error appears schema-related.
    """
    # Skip logging for expected "user not found" - not caching is correct
    if str(error) == "" and type(error).__name__ == "Exception":
        return
    err_str = str(error).lower()
    hint = ""
    if any(
        x in err_str
        for x in ("column", "schema", "does not exist", "prisma", "migrate")
    ):
        hint = (
            " Run `prisma db push` or `prisma migrate deploy` to fix schema mismatches."
        )
    verbose_proxy_logger.error(
        f"Budget lookup failed for {entity}; cache will not be populated. "
        f"Each request will hit the database. Error: {error}.{hint}"
    )

