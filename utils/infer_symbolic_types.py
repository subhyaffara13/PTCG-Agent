
def infer_symbolic_types(traced):
    """
    Calls our symbolic inferencer twice.
    This is useful when one pass is not enough
    to infer all the information such as the case
    for broadcasting.
    """
    r = Refine(traced)
    r.refine()
    mgu = unify_eq(r.constraints)
    substitute_all_types(traced.graph, mgu)

    r = Refine(traced)
    r.refine()
    mgu = unify_eq(r.constraints)
    substitute_all_types(traced.graph, mgu)

    r.symbolic_relations()

