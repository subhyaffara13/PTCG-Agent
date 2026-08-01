
def parse_partition_upper_bound(bound_expr: str) -> Optional[datetime]:
    """
    Upper bound of a Postgres partition from its `pg_get_expr(relpartbound)`
    string, e.g. "FOR VALUES FROM ('2026-06-01 00:00:00') TO ('2026-06-02 00:00:00')".
    Returns None for the DEFAULT partition or anything we cannot parse, so such
    partitions are never selected for dropping.
    """
    if "DEFAULT" in bound_expr.upper():
        return None
    match = _BOUND_UPPER_RE.search(bound_expr)
    if match is None:
        return None
    try:
        return datetime.fromisoformat(match.group(1))
    except ValueError:
        return None

