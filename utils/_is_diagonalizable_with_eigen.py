
def _is_diagonalizable_with_eigen(M, reals_only=False):
    """See _is_diagonalizable. This function returns the bool along with the
    eigenvectors to avoid calculating them again in functions like
    ``diagonalize``."""

    if not M.is_square:
        return False, []

    eigenvecs = M.eigenvects(simplify=True)

    for val, mult, basis in eigenvecs:
        if reals_only and not val.is_real: # if we have a complex eigenvalue
            return False, eigenvecs

        if mult != len(basis): # if the geometric multiplicity doesn't equal the algebraic
            return False, eigenvecs

    return True, eigenvecs

