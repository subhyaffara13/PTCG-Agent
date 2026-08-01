
def dmp_content(f, u, K):
    """
    Returns GCD of multivariate coefficients.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y, = ring("x,y", ZZ)

    >>> R.dmp_content(2*x*y + 6*x + 4*y + 12)
    2*y + 6

    """
    cont, v = dmp_LC(f, K), u - 1

    if dmp_zero_p(f, u):
        return cont

    for c in f[1:]:
        cont = dmp_gcd(cont, c, v, K)

        if dmp_one_p(cont, v, K):
            break

    if K.is_negative(dmp_ground_LC(cont, v, K)):
        return dmp_neg(cont, v, K)
    else:
        return cont

