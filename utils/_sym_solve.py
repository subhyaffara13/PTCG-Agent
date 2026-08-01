
def _sym_solve(Dinv, A, r1, r2, solve):
    """
    An implementation of [4] equation 8.31 and 8.32

    References
    ----------
    .. [4] Andersen, Erling D., and Knud D. Andersen. "The MOSEK interior point
           optimizer for linear programming: an implementation of the
           homogeneous algorithm." High performance optimization. Springer US,
           2000. 197-232.

    """
    # [4] 8.31
    r = r2 + A.dot(Dinv * r1)
    v = solve(r)
    # [4] 8.32
    u = Dinv * (A.T.dot(v) - r1)
    return u, v

