
def _rewrite1(f, x, recursive=True):
    """
    Try to rewrite ``f`` using a (sum of) single G functions with argument a*x**b.
    Return fac, po, g such that f = fac*po*g, fac is independent of ``x``.
    and po = x**s.
    Here g is a result from _rewrite_single.
    Return None on failure.
    """
    fac, po, g = _split_mul(f, x)
    g = _rewrite_single(g, x, recursive)
    if g:
        return fac, po, g[0], g[1]

