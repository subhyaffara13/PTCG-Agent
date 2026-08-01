
def dup_inner_subresultants(f, g, K):
    """
    Subresultant PRS algorithm in `K[x]`.

    Computes the subresultant polynomial remainder sequence (PRS)
    and the non-zero scalar subresultants of `f` and `g`.
    By [1] Thm. 3, these are the constants '-c' (- to optimize
    computation of sign).
    The first subdeterminant is set to 1 by convention to match
    the polynomial and the scalar subdeterminants.
    If 'deg(f) < deg(g)', the subresultants of '(g,f)' are computed.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_inner_subresultants(x**2 + 1, x**2 - 1)
    ([x**2 + 1, x**2 - 1, -2], [1, 1, 4])

    References
    ==========

    .. [1] W.S. Brown, The Subresultant PRS Algorithm.
           ACM Transaction of Mathematical Software 4 (1978) 237-249

    """
    n = dup_degree(f)
    m = dup_degree(g)

    if n < m:
        f, g = g, f
        n, m = m, n

    if not f:
        return [], []

    if not g:
        return [f], [K.one]

    R = [f, g]
    d = n - m

    b = (-K.one)**(d + 1)

    h = dup_prem(f, g, K)
    h = dup_mul_ground(h, b, K)

    lc = dup_LC(g, K)
    c = lc**d

    # Conventional first scalar subdeterminant is 1
    S = [K.one, c]
    c = -c

    while h:
        k = dup_degree(h)
        R.append(h)

        f, g, m, d = g, h, k, m - k

        b = -lc * c**d

        h = dup_prem(f, g, K)
        h = dup_quo_ground(h, b, K)

        lc = dup_LC(g, K)

        if d > 1:        # abnormal case
            q = c**(d - 1)
            c = K.quo((-lc)**d, q)
        else:
            c = -lc

        S.append(-c)

    return R, S

