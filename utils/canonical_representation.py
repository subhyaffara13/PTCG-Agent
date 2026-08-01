
def canonical_representation(a, d, DE):
    """
    Canonical Representation.

    Explanation
    ===========

    Given a derivation D on k[t] and f = a/d in k(t), return (f_p, f_s,
    f_n) in k[t] x k(t) x k(t) such that f = f_p + f_s + f_n is the
    canonical representation of f (f_p is a polynomial, f_s is reduced
    (has a special denominator), and f_n is simple (has a normal
    denominator).
    """
    # Make d monic
    l = Poly(1/d.LC(), DE.t)
    a, d = a.mul(l), d.mul(l)

    q, r = a.div(d)
    dn, ds = splitfactor(d, DE)

    b, c = gcdex_diophantine(dn.as_poly(DE.t), ds.as_poly(DE.t), r.as_poly(DE.t))
    b, c = b.as_poly(DE.t), c.as_poly(DE.t)

    return (q, (b, ds), (c, dn))

