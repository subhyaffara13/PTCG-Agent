
def try_restrict_literal_union(t: UnionType, s: Type) -> list[Type] | None:
    """Return the items of t, excluding any occurrence of s, if and only if
      - t only contains simple literals
      - s is a simple literal

    Otherwise, returns None
    """
    ps = get_proper_type(s)
    if not mypy.typeops.is_simple_literal(ps):
        return None

    new_items: list[Type] = []
    for i in t.relevant_items():
        pi = get_proper_type(i)
        if not mypy.typeops.is_simple_literal(pi):
            return None
        if pi != ps:
            new_items.append(i)
    return new_items

