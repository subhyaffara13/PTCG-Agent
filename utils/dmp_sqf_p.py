
def dmp_sqf_p(f, u, K):
    """
    Return ``True`` if ``f`` is a square-free polynomial in ``K[X]``.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y = ring("x,y", ZZ)

    >>> R.dmp_sqf_p(x**2 + 2*x*y + y**2)
    False
    >>> R.dmp_sqf_p(x**2 + y**2)
    True

    """
    if dmp_zero_p(f, u):
        return True

    for i in range(u+1):

        fp = dmp_diff_in(f, 1, i, u, K)

        if dmp_zero_p(fp, u):
            continue

        gcd = dmp_gcd(f, fp, u, K)

        if dmp_degree_in(gcd, i, u) != 0:
            return False

    return True

