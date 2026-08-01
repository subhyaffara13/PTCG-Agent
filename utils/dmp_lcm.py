
def dmp_lcm(f, g, u, K):
    """
    Computes polynomial LCM of `f` and `g` in `K[X]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x,y, = ring("x,y", ZZ)

    >>> f = x**2 + 2*x*y + y**2
    >>> g = x**2 + x*y

    >>> R.dmp_lcm(f, g)
    x**3 + 2*x**2*y + x*y**2

    """
    if not u:
        return dup_lcm(f, g, K)

    if K.is_Field:
        return dmp_ff_lcm(f, g, u, K)
    else:
        return dmp_rr_lcm(f, g, u, K)

