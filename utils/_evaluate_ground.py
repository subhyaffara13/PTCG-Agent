
def _evaluate_ground(f, i, a):
    r"""
    Evaluate a polynomial `f` at `a` in the `i`-th variable of the ground
    domain.
    """
    ring = f.ring.clone(domain=f.ring.domain.ring.drop(i))
    fa = ring.zero

    for monom, coeff in f.iterterms():
        fa[monom] = coeff.evaluate(i, a)

    return fa

