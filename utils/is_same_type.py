
def is_same_type(
    a: Type, b: Type, ignore_promotions: bool = True, subtype_context: SubtypeContext | None = None
) -> bool:
    """Are these types proper subtypes of each other?

    This means types may have different representation (e.g. an alias, or
    a non-simplified union) but are semantically exchangeable in all contexts.
    """
    # First, use fast path for some common types. This is performance-critical.
    if (
        type(a) is Instance
        and type(b) is Instance
        and a.type == b.type
        and len(a.args) == len(b.args)
        and a.last_known_value is b.last_known_value
    ):
        return all(is_same_type(x, y) for x, y in zip(a.args, b.args))
    elif (
        isinstance(a, TypeVarType)
        and isinstance(b, TypeVarType)
        and a.id == b.id
        and a.upper_bound == b.upper_bound
    ):
        return True

    # Note that using ignore_promotions=True (default) makes types like int and int64
    # considered not the same type (which is the case at runtime).
    # Also Union[bool, int] (if it wasn't simplified before) will be different
    # from plain int, etc.
    return is_proper_subtype(
        a, b, ignore_promotions=ignore_promotions, subtype_context=subtype_context
    ) and is_proper_subtype(
        b, a, ignore_promotions=ignore_promotions, subtype_context=subtype_context
    )


def is_same_type(a: RType, b: RType) -> bool:
    return a.accept(SameTypeVisitor(b))

