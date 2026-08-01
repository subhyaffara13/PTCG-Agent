
def _fuzzy_positive_semidefinite(M):
    nonnegative_diagonals = M._has_nonnegative_diagonals()
    if nonnegative_diagonals is False:
        return False

    if nonnegative_diagonals and M.is_weakly_diagonally_dominant:
        return True

    return None

