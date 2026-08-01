
def _extract_dialect(kwds: dict[str, str | csv.Dialect]) -> csv.Dialect | None:
    """
    Extract concrete csv dialect instance.

    Returns
    -------
    csv.Dialect or None
    """
    if kwds.get("dialect") is None:
        return None

    dialect = kwds["dialect"]
    if isinstance(dialect, str) and dialect in csv.list_dialects():
        # get_dialect is typed to return a `_csv.Dialect` for some reason in typeshed
        tdialect = cast(csv.Dialect, csv.get_dialect(dialect))
        _validate_dialect(tdialect)

    else:
        _validate_dialect(dialect)
        tdialect = cast(csv.Dialect, dialect)

    return tdialect

