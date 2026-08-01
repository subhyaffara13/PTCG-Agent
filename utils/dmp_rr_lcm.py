
def dmp_rr_lcm(f, g, u, K):
    """
    Computes polynomial LCM over a ring in `K[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y, = ring("x,y", ZZ)

    >>> f = x**2 + 2*x*y + y**2
    >>> g = x**2 + x*y

    >>> R.dmp_rr_lcm(f, g)
    x**3 + 2*x**2*y + x*y**2

    """
    fc, f = dmp_ground_primitive(f, u, K)
    gc, g = dmp_ground_primitive(g, u, K)

    c = K.lcm(fc, gc)

    h = dmp_quo(dmp_mul(f, g, u, K),
                dmp_gcd(f, g, u, K), u, K)

    return dmp_mul_ground(h, c, u, K)

