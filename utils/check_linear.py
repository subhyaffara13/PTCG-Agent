
def check_linear(scc: set[TypeVarId], lowers: Bounds, uppers: Bounds) -> bool:
    """Check there are only linear constraints between type variables in SCC.

    Linear are constraints like T <: S (while T <: F[S] are non-linear).
    """
    for tv in scc:
        if any(get_vars(lt, list(scc)) for lt in lowers[tv]):
            return False
        if any(get_vars(ut, list(scc)) for ut in uppers[tv]):
            return False
    return True

