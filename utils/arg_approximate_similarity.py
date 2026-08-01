
def arg_approximate_similarity(actual: Type, formal: Type) -> bool:
    """Return if caller argument (actual) is roughly compatible with signature arg (formal).

    This function is deliberately loose and will report two types are similar
    as long as their "shapes" are plausibly the same.

    This is useful when we're doing error reporting: for example, if we're trying
    to select an overload alternative and there's no exact match, we can use
    this function to help us identify which alternative the user might have
    *meant* to match.
    """
    actual = get_proper_type(actual)
    formal = get_proper_type(formal)

    # Erase typevars: we'll consider them all to have the same "shape".
    if isinstance(actual, TypeVarType):
        actual = erase_to_union_or_bound(actual)
    if isinstance(formal, TypeVarType):
        formal = erase_to_union_or_bound(formal)

    # Callable or Type[...]-ish types
    def is_typetype_like(typ: ProperType) -> bool:
        return (
            isinstance(typ, TypeType)
            or (isinstance(typ, FunctionLike) and typ.is_type_obj())
            or (isinstance(typ, Instance) and typ.type.fullname == "builtins.type")
        )

    if isinstance(formal, CallableType):
        if isinstance(actual, (CallableType, Overloaded, TypeType)):
            return True
    if is_typetype_like(actual) and is_typetype_like(formal):
        return True

    # Unions
    if isinstance(actual, UnionType):
        return any(arg_approximate_similarity(item, formal) for item in actual.relevant_items())
    if isinstance(formal, UnionType):
        return any(arg_approximate_similarity(actual, item) for item in formal.relevant_items())

    # TypedDicts
    if isinstance(actual, TypedDictType):
        if isinstance(formal, TypedDictType):
            return True
        return arg_approximate_similarity(actual.fallback, formal)

    # Instances
    # For instances, we mostly defer to the existing is_subtype check.
    if isinstance(formal, Instance):
        if isinstance(actual, CallableType):
            actual = actual.fallback
        if isinstance(actual, Overloaded):
            actual = actual.items[0].fallback
        if isinstance(actual, TupleType):
            actual = tuple_fallback(actual)
        if isinstance(actual, Instance) and formal.type in actual.type.mro:
            # Try performing a quick check as an optimization
            return True

    # Fall back to a standard subtype check for the remaining kinds of type.
    return is_subtype(erasetype.erase_type(actual), erasetype.erase_type(formal))

