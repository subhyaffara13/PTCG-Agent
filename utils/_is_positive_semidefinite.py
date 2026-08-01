
def _is_positive_semidefinite(M):
    if not M.is_hermitian:
        if not M.is_square:
            return False
        M = M + M.H

    fuzzy = _fuzzy_positive_semidefinite(M)
    if fuzzy is not None:
        return fuzzy

    return _is_positive_semidefinite_cholesky(M)

