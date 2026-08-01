
def _is_positive_definite(M):
    if not M.is_hermitian:
        if not M.is_square:
            return False
        M = M + M.H

    fuzzy = _fuzzy_positive_definite(M)
    if fuzzy is not None:
        return fuzzy

    return _is_positive_definite_GE(M)

