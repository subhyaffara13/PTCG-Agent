
def puiseux_ring(
    symbols: str | list[Expr], domain: Domain
) -> tuple[PuiseuxRing, Unpack[tuple[PuiseuxPoly, ...]]]:
    """Construct a Puiseux ring.

    This function constructs a Puiseux ring with the given symbols and domain.

    >>> from sympy.polys.domains import QQ
    >>> from sympy.polys.puiseux import puiseux_ring
    >>> R, x, y = puiseux_ring('x y', QQ)
    >>> R
    PuiseuxRing((x, y), QQ)
    >>> p = 5*x**QQ(1,2) + 7/y
    >>> p
    7*y**(-1) + 5*x**(1/2)
    """
    ring = PuiseuxRing(symbols, domain)
    return (ring,) + ring.gens # type: ignore

