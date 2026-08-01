
def solve_one(lowers: Iterable[Type], uppers: Iterable[Type]) -> Type | None:
    """Solve constraints by finding by using meets of upper bounds, and joins of lower bounds."""

    candidate: Type | None = None

    # Filter out previous results of failed inference, they will only spoil the current pass...
    new_uppers = []
    for u in uppers:
        pu = get_proper_type(u)
        if not isinstance(pu, UninhabitedType) or not pu.ambiguous:
            new_uppers.append(u)
    uppers = new_uppers

    # ...unless this is the only information we have, then we just pass it on.
    lowers = list(lowers)
    if not uppers and not lowers:
        candidate = UninhabitedType()
        candidate.ambiguous = True
        return candidate

    bottom: Type | None = None
    top: Type | None = None

    # Process each bound separately, and calculate the lower and upper
    # bounds based on constraints. Note that we assume that the constraint
    # targets do not have constraint references.
    if type_state.infer_unions and lowers:
        # This deviates from the general mypy semantics because
        # recursive types are union-heavy in 95% of cases.
        # Retain `None` when no bottoms were provided to avoid bogus `Never` inference.
        bottom = UnionType.make_union(lowers)
    else:
        # The order of lowers is non-deterministic.
        # We attempt to sort lowers because joins are non-associative. For instance:
        # join(join(int, str), int | str) == join(object, int | str) == object
        # join(int, join(str, int | str)) == join(int, int | str)    == int | str
        # Note that joins in theory should be commutative, but in practice some bugs mean this is
        # also a source of non-deterministic type checking results.
        sorted_lowers = sorted(lowers, key=_join_sorted_key)
        if sorted_lowers:
            bottom = join_type_list(sorted_lowers)

    for target in uppers:
        if top is None:
            top = target
        else:
            top = meet_types(top, target)

    p_top = get_proper_type(top)
    p_bottom = get_proper_type(bottom)
    if isinstance(p_top, AnyType) or isinstance(p_bottom, AnyType):
        source_any = top if isinstance(p_top, AnyType) else bottom
        assert isinstance(source_any, ProperType) and isinstance(source_any, AnyType)
        return AnyType(TypeOfAny.from_another_any, source_any=source_any)
    elif bottom is None:
        if top:
            candidate = top
        else:
            # No constraints for type variable
            return None
    elif top is None:
        candidate = bottom
    elif is_subtype(bottom, top):
        candidate = bottom
    else:
        candidate = None
    return candidate

