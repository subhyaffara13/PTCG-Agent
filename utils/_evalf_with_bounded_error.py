
def _evalf_with_bounded_error(x: Expr, eps: Expr | None = None,
                              m: int = 0,
                              options: OPT_DICT | None = None) -> TMP_RES:
    """
    Evaluate *x* to within a bounded absolute error.

    Parameters
    ==========

    x : Expr
        The quantity to be evaluated.
    eps : Expr, None, optional (default=None)
        Positive real upper bound on the acceptable error.
    m : int, optional (default=0)
        If *eps* is None, then use 2**(-m) as the upper bound on the error.
    options: OPT_DICT
        As in the ``evalf`` function.

    Returns
    =======

    A tuple ``(re, im, re_acc, im_acc)``, as returned by ``evalf``.

    See Also
    ========

    evalf

    """
    if eps is not None:
        if not (eps.is_Rational or eps.is_Float) or not eps > 0:
            raise ValueError("eps must be positive")
        r, _, _, _ = evalf(1/eps, 1, {})
        m = fastlog(r)

    c, d, _, _ = evalf(x, 1, {})
    # Note: If x = a + b*I, then |a| <= 2|c| and |b| <= 2|d|, with equality
    # only in the zero case.
    # If a is non-zero, then |c| = 2**nc for some integer nc, and c has
    # bitcount 1. Therefore 2**fastlog(c) = 2**(nc+1) = 2|c| is an upper bound
    # on |a|. Likewise for b and d.
    nr, ni = fastlog(c), fastlog(d)
    n = max(nr, ni) + 1
    # If x is 0, then n is MINUS_INF, and p will be 1. Otherwise,
    # n - 1 bits get us past the integer parts of a and b, and +1 accounts for
    # the factor of <= sqrt(2) that is |x|/max(|a|, |b|).
    p = max(1, m + n + 1)

    options = options or {}
    return evalf(x, p, options)

