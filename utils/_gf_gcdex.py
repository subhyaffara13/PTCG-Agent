
def _gf_gcdex(f, g, p):
    r"""
    Extended Euclidean Algorithm for two univariate polynomials over
    `\mathbb Z_p`.

    Returns polynomials `s, t` and `h`, such that `h` is the GCD of `f` and
    `g` and `sf + tg = h \; \mathrm{mod} \, p`.

    """
    ring = f.ring
    s, t, h = gf_gcdex(f.to_dense(), g.to_dense(), p, ring.domain)
    return ring.from_dense(s), ring.from_dense(t), ring.from_dense(h)

