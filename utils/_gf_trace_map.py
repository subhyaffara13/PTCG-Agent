
def _gf_trace_map(f, n, g, b, p, K):
    """
    utility for ``gf_edf_shoup``
    """
    f = gf_rem(f, g, p, K)
    h = f
    r = f
    for i in range(1, n):
        h = gf_frobenius_map(h, g, b, p, K)
        r = gf_add(r, h, p, K)
        r = gf_rem(r, g, p, K)
    return r

