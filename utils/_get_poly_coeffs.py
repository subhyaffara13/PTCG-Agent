
def _get_poly_coeffs(poly, order):
    cs = [0 for _ in range(order+1)]
    for c, m in zip(poly.coeffs(), poly.monoms()):
        cs[-1-m[0]] = c
    return cs

