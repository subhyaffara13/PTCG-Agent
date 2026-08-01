
def recursively_defined_type_refs() -> set[str]:
    visited = _generic_recursion_cache.get()
    if not visited:
        return set()  # not in a generic recursion, so there are no types

    return visited.copy()  # don't allow modifications

