
def dup_lcm(f, g, K):
    """
    Computes polynomial LCM of `f` and `g` in `K[x]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_lcm(x**2 - 1, x**2 - 3*x + 2)
    x**3 - 2*x**2 - x + 2

    """
    if K.is_Field:
        return dup_ff_lcm(f, g, K)
    else:
        return dup_rr_lcm(f, g, K)

