
def pow_xin(p, i, n):
    """
    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.puiseux import puiseux_ring
    >>> from sympy.polys.ring_series import pow_xin
    >>> R, x, y = puiseux_ring('x, y', QQ)
    >>> p = x**QQ(2,5) + x + x**QQ(2,3)
    >>> index = p.ring.gens.index(x)
    >>> pow_xin(p, index, 15)
    x**6 + x**10 + x**15
    """
    R = p.ring
    q = {}
    for k, v in p.terms():
        k1 = list(k)
        k1[i] *= n
        q[tuple(k1)] = v
    return R(q)

