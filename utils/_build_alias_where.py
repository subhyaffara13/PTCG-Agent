
def _build_alias_where(field: str, patterns: list) -> dict:
    """Build a Prisma ``where`` clause for alias patterns.

    Supports exact matches and suffix wildcards (``prefix*``).
    Returns something like:
        {"OR": [{"field": {"in": ["a","b"]}}, {"field": {"startsWith": "dev-"}}]}
    """
    exact: list = []
    prefix_conditions: list = []
    for pat in patterns:
        if pat.endswith("*"):
            prefix_conditions.append({field: {"startsWith": pat[:-1]}})
        else:
            exact.append(pat)

    conditions: list = []
    if exact:
        conditions.append({field: {"in": exact}})
    conditions.extend(prefix_conditions)

    if not conditions:
        return {field: {"not": None}}
    if len(conditions) == 1:
        return conditions[0]
    return {"OR": conditions}

