
def is_recursive_pair(s: Type, t: Type) -> bool:
    """Is this a pair of recursive types?

    There may be more cases, and we may be forced to use e.g. has_recursive_types()
    here, but this function is called in very hot code, so we try to keep it simple
    and return True only in cases we know may have problems.
    """
    if isinstance(s, TypeAliasType) and s.is_recursive:
        return (
            isinstance(get_proper_type(t), (Instance, UnionType))
            or isinstance(t, TypeAliasType)
            and t.is_recursive
            # Tuple types are special, they can cause an infinite recursion even if
            # the other type is not recursive, because of the tuple fallback that is
            # calculated "on the fly".
            or isinstance(get_proper_type(s), TupleType)
        )
    if isinstance(t, TypeAliasType) and t.is_recursive:
        return (
            isinstance(get_proper_type(s), (Instance, UnionType))
            or isinstance(s, TypeAliasType)
            and s.is_recursive
            # Same as above.
            or isinstance(get_proper_type(t), TupleType)
        )
    return False

