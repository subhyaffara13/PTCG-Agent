
def collect_all_named_types(t: Type) -> list[Type]:
    """Return all instances/aliases/type variables that `t` contains (including `t`).

    This is similar to collect_all_inner_types from typeanal but only
    returns instances and will recurse into fallbacks.
    """
    visitor = CollectAllNamedTypesQuery()
    t.accept(visitor)
    return visitor.types

