
def dup_discriminant(f, K):
    """
    Computes discriminant of a polynomial in `K[x]`.

    Examples
    ========

    >>> from sympy.polys import ring, ZZ
    >>> R, x = ring("x", ZZ)

    >>> R.dup_discriminant(x**2 + 2*x + 3)
    -8

    """
    d = dup_degree(f)

    if d <= 0:
        return K.zero
    else:
        s = (-1)**((d*(d - 1)) // 2)
        c = dup_LC(f, K)

        r = dup_resultant(f, dup_diff(f, 1, K), K)

        return K.quo(r, c*K(s))

