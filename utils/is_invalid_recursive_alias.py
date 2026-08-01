
def is_invalid_recursive_alias(seen_nodes: set[TypeAlias], target: Type) -> bool:
    """Flag aliases like A = Union[int, A], T = tuple[int, *T] (and similar mutual aliases).

    Such aliases don't make much sense, and cause problems in later phases.
    """
    if isinstance(target, TypeAliasType):
        if target.alias in seen_nodes:
            return True
        assert target.alias, f"Unfixed type alias {target.type_ref}"
        return is_invalid_recursive_alias(seen_nodes | {target.alias}, get_proper_type(target))
    assert isinstance(target, ProperType)
    if not isinstance(target, (UnionType, TupleType)):
        return False
    if isinstance(target, UnionType):
        return any(is_invalid_recursive_alias(seen_nodes, item) for item in target.items)
    for item in target.items:
        if isinstance(item, UnpackType):
            if is_invalid_recursive_alias(seen_nodes, item.type):
                return True
    return False

