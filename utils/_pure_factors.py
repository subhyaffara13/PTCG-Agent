
def _pure_factors(poly):
    _, factors = poly.factor_list()
    return [(PurePoly(f, expand=False), m) for f, m in factors]

