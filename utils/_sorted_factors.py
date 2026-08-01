
def _sorted_factors(factors, method):
    """Sort a list of ``(expr, exp)`` pairs. """
    if method == 'sqf':
        def key(obj):
            poly, exp = obj
            rep = poly.rep.to_list()
            return (exp, len(rep), len(poly.gens), str(poly.domain), rep)
    else:
        def key(obj):
            poly, exp = obj
            rep = poly.rep.to_list()
            return (len(rep), len(poly.gens), exp, str(poly.domain), rep)

    return sorted(factors, key=key)

