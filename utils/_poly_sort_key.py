
def _poly_sort_key(poly):
    """Sort a list of polys."""
    rep = poly.rep.to_list()
    return (len(rep), len(poly.gens), str(poly.domain), rep)


def _poly_sort_key(poly):
    """Sort key for polynomials"""
    if poly.domain.is_FF:
        poly = poly.set_domain(ZZ)
    return poly.degree_list(), poly.rep.to_list()

