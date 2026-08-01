
def _gf_div(f, g, p):
    r"""
    Compute `\frac f g` modulo `p` for two univariate polynomials over
    `\mathbb Z_p`.
    """
    ring = f.ring
    densequo, denserem = gf_div(f.to_dense(), g.to_dense(), p, ring.domain)
    return ring.from_dense(densequo), ring.from_dense(denserem)

