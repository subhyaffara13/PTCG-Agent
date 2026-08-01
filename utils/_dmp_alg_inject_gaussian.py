
def _dmp_alg_inject_gaussian(f, u, K):
    """Helper function for :func:`dmp_alg_inject`."""
    f, h = dmp_to_dict(f, u), {}

    for f_monom, g in f.items():
        x, y = g.x, g.y
        if x:
            h[(0,) + f_monom] = x
        if y:
            h[(1,) + f_monom] = y

    F = dmp_from_dict(h, u + 1, K.dom)

    return F, u + 1, K.dom

