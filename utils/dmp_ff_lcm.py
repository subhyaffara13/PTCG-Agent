
def dmp_ff_lcm(f, g, u, K):
    """
    Computes polynomial LCM over a field in `K[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x,y, = ring("x,y", QQ)

    >>> f = QQ(1,4)*x**2 + x*y + y**2
    >>> g = QQ(1,2)*x**2 + x*y

    >>> R.dmp_ff_lcm(f, g)
    x**3 + 4*x**2*y + 4*x*y**2

    """
    h = dmp_quo(dmp_mul(f, g, u, K),
                dmp_gcd(f, g, u, K), u, K)

    return dmp_ground_monic(h, u, K)

