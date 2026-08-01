
def rs_is_puiseux(p, x):
    """
    Test if ``p`` is Puiseux series in ``x``.

    Raise an exception if it has a negative power in ``x``.

    Examples
    ========

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.puiseux import puiseux_ring
    >>> from sympy.polys.ring_series import rs_is_puiseux
    >>> R, x = puiseux_ring('x', QQ)
    >>> p = x**QQ(2,5) + x**QQ(2,3) + x
    >>> rs_is_puiseux(p, x)
    True
    """
    index = p.ring.gens.index(x)
    for k in p.itermonoms():
        if k[index] != int(k[index]):
            return True
        if k[index] < 0:
            raise ValueError('The series is not regular in %s' % x)
    return False

