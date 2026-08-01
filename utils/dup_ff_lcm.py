
def dup_ff_lcm(f, g, K):
    """
    Computes polynomial LCM over a field in `K[x]`.

    Examples
    ========

    >>> from sympy.polys import ring, QQ
    >>> R, x = ring("x", QQ)

    >>> f = QQ(1,2)*x**2 + QQ(7,4)*x + QQ(3,2)
    >>> g = QQ(1,2)*x**2 + x

    >>> R.dup_ff_lcm(f, g)
    x**3 + 7/2*x**2 + 3*x

    """
    h = dup_quo(dup_mul(f, g, K),
                dup_gcd(f, g, K), K)

    return dup_monic(h, K)

