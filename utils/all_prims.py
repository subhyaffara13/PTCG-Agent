
def all_prims() -> set[Any]:
    """
    Set of all prim functions, e.g., torch._prims.add in all_prims()
    """
    return {torch._prims.__dict__.get(s) for s in torch._prims.__all__}

