
def _dmp_alg_inject_alg(f, u, K):
    """Helper function for :func:`dmp_alg_inject`."""
    f, h = dmp_to_dict(f, u), {}

    for f_monom, g in f.items():
        for g_monom, c in g.to_dict().items():
            h[g_monom + f_monom] = c

    F = dmp_from_dict(h, u + 1, K.dom)

    return F, u + 1, K.dom

