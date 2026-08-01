
def _eigenspace(M, eigenval, iszerofunc=_iszero, simplify=False):
    """Get a basis for the eigenspace for a particular eigenvalue"""
    m   = M - M.eye(M.rows) * eigenval
    ret = m.nullspace(iszerofunc=iszerofunc)

    # The nullspace for a real eigenvalue should be non-trivial.
    # If we didn't find an eigenvector, try once more a little harder
    if len(ret) == 0 and simplify:
        ret = m.nullspace(iszerofunc=iszerofunc, simplify=True)
    if len(ret) == 0:
        raise NotImplementedError(
            "Can't evaluate eigenvector for eigenvalue {}".format(eigenval))
    return ret

