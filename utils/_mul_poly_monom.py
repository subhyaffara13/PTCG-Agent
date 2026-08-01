
def _mul_poly_monom(poly: PolyElement, monom: Iterable[int]) -> PolyElement:
    ring = poly.ring
    mul = ring.monomial_mul
    return ring.from_dict({mul(m, monom): c for m, c in poly.terms()})

