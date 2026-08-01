
def _div_poly_monom(poly: PolyElement, monom: Iterable[int]) -> PolyElement:
    ring = poly.ring
    div = ring.monomial_div
    return ring.from_dict({div(m, monom): c for m, c in poly.terms()})

