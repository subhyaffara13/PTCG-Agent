
def dmp_zz_collins_resultant(f, g, u, K):
    """
    Collins's modular resultant algorithm in `Z[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> f = x + y + 2
    >>> g = 2*x*y + x + 3

    >>> R.dmp_zz_collins_resultant(f, g)
    -2*y**2 - 5*y + 1

    """

    n = dmp_degree(f, u)
    m = dmp_degree(g, u)

    if n < 0 or m < 0:
        return dmp_zero(u - 1)

    A = dmp_max_norm(f, u, K)
    B = dmp_max_norm(g, u, K)

    a = dmp_ground_LC(f, u, K)
    b = dmp_ground_LC(g, u, K)

    v = u - 1

    B = K(2)*K.factorial(K(n + m))*A**m*B**n
    r, p, P = dmp_zero(v), K.one, K.one

    from sympy.ntheory import nextprime

    while P <= B:
        p = K(nextprime(p))

        while not (a % p) or not (b % p):
            p = K(nextprime(p))

        F = dmp_ground_trunc(f, p, u, K)
        G = dmp_ground_trunc(g, p, u, K)

        try:
            R = dmp_zz_modular_resultant(F, G, p, u, K)
        except HomomorphismFailed:
            continue

        if K.is_one(P):
            r = R
        else:
            r = dmp_apply_pairs(r, R, _collins_crt, (P, p, K), v, K)

        P *= p

    return r

