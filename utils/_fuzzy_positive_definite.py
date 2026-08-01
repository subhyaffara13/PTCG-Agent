
def _fuzzy_positive_definite(M):
    positive_diagonals = M._has_positive_diagonals()
    if positive_diagonals is False:
        return False

    if positive_diagonals and M.is_strongly_diagonally_dominant:
        return True

    return None

