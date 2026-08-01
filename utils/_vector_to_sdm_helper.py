
def _vector_to_sdm_helper(v, order):
    """Helper method for common code in Global and Local poly rings."""
    from sympy.polys.distributedmodules import sdm_from_dict
    d = {}
    for i, e in enumerate(v):
        for key, value in e.to_dict().items():
            d[(i,) + key] = value
    return sdm_from_dict(d, order)

