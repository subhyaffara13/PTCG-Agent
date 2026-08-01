
def _log_context(
    *,
    user: bool = False,
    home: str | None = None,
    root: str | None = None,
    prefix: str | None = None,
) -> None:
    parts = [
        "Additional context:",
        "user = %r",
        "home = %r",
        "root = %r",
        "prefix = %r",
    ]

    logger.log(_MISMATCH_LEVEL, "\n".join(parts), user, home, root, prefix)

