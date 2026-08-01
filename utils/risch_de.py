
def rischDE(fa, fd, ga, gd, DE):
    """
    Solve a Risch Differential Equation: Dy + f*y == g.

    Explanation
    ===========

    See the outline in the docstring of rde.py for more information
    about the procedure used.  Either raise NonElementaryIntegralException, in
    which case there is no solution y in the given differential field,
    or return y in k(t) satisfying Dy + f*y == g, or raise
    NotImplementedError, in which case, the algorithms necessary to
    solve the given Risch Differential Equation have not yet been
    implemented.
    """
    _, (fa, fd) = weak_normalizer(fa, fd, DE)
    a, (ba, bd), (ca, cd), hn = normal_denom(fa, fd, ga, gd, DE)
    A, B, C, hs = special_denom(a, ba, bd, ca, cd, DE)
    try:
        # Until this is fully implemented, use oo.  Note that this will almost
        # certainly cause non-termination in spde() (unless A == 1), and
        # *might* lead to non-termination in the next step for a nonelementary
        # integral (I don't know for certain yet).  Fortunately, spde() is
        # currently written recursively, so this will just give
        # RuntimeError: maximum recursion depth exceeded.
        n = bound_degree(A, B, C, DE)
    except NotImplementedError:
        # Useful for debugging:
        # import warnings
        # warnings.warn("rischDE: Proceeding with n = oo; may cause "
        #     "non-termination.")
        n = oo

    B, C, m, alpha, beta = spde(A, B, C, n, DE)
    if C.is_zero:
        y = C
    else:
        y = solve_poly_rde(B, C, m, DE)

    return (alpha*y + beta, hn*hs)

