
def gmres_loose(A, b, tol):
    """
    gmres with looser termination condition.
    """
    b = np.asarray(b)
    min_tol = 1000 * np.sqrt(b.size) * np.finfo(b.dtype).eps
    return gmres(A, b, rtol=max(tol, min_tol), atol=0)

