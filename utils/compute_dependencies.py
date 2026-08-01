
def compute_dependencies(
    tvars: list[TypeVarId], graph: Graph, lowers: Bounds, uppers: Bounds
) -> dict[TypeVarId, list[TypeVarId]]:
    """Compute dependencies between type variables induced by constraints.

    If we have a constraint like T <: List[S], we say that T depends on S, since
    we will need to solve for S first before we can solve for T.
    """
    res = {}
    for tv in tvars:
        deps = set()
        for lt in lowers[tv]:
            deps |= get_vars(lt, tvars)
        for ut in uppers[tv]:
            deps |= get_vars(ut, tvars)
        for other in tvars:
            if other == tv:
                continue
            if (tv, other) in graph or (other, tv) in graph:
                deps.add(other)
        res[tv] = list(deps)
    return res

