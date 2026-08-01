
def choose_free(
    scc: list[TypeVarLikeType], original_vars: list[TypeVarId]
) -> TypeVarLikeType | None:
    """Choose the best solution for an SCC containing only type variables.

    This is needed to preserve e.g. the upper bound in a situation like this:
        def dec(f: Callable[[T], S]) -> Callable[[T], S]: ...

        @dec
        def test(x: U) -> U: ...

    where U <: A.
    """

    if len(scc) == 1:
        # Fast path, choice is trivial.
        return scc[0]

    common_upper_bound = meet_type_list([t.upper_bound for t in scc])
    common_upper_bound_p = get_proper_type(common_upper_bound)
    # We include None for when strict-optional is disabled.
    if isinstance(common_upper_bound_p, (UninhabitedType, NoneType)):
        # This will cause to infer Never, which is better than a free TypeVar
        # that has an upper bound Never.
        return None

    values: list[Type] = []
    for tv in scc:
        if isinstance(tv, TypeVarType) and tv.values:
            if values:
                # It is too tricky to support multiple TypeVars with values
                # within the same SCC.
                return None
            values = tv.values.copy()

    if values and not is_trivial_bound(common_upper_bound_p):
        # If there are both values and upper bound present, we give up,
        # since type variables having both are not supported.
        return None

    # For convenience with current type application machinery, we use a stable
    # choice that prefers the original type variables (not polymorphic ones) in SCC.
    best = min(scc, key=lambda x: (x.id not in original_vars, x.id.raw_id))
    if isinstance(best, TypeVarType):
        return best.copy_modified(values=values, upper_bound=common_upper_bound)
    if is_trivial_bound(common_upper_bound_p, allow_tuple=True):
        # TODO: support more cases for ParamSpecs/TypeVarTuples
        return best
    return None

