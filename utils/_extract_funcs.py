
def _extract_funcs(eqs):
    funcs = []
    for eq in eqs:
        derivs = [node for node in preorder_traversal(eq) if isinstance(node, Derivative)]
        func = []
        for d in derivs:
            func += list(d.atoms(AppliedUndef))
        for func_ in func:
            funcs.append(func_)
    funcs = list(uniq(funcs))

    return funcs

