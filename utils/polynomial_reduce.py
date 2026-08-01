
def polynomial_reduce(p, DE):
    """
    Polynomial Reduction.

    Explanation
    ===========

    Given a derivation D on k(t) and p in k[t] where t is a nonlinear
    monomial over k, return q, r in k[t] such that p = Dq  + r, and
    deg(r) < deg_t(Dt).
    """
    q = Poly(0, DE.t)
    while p.degree(DE.t) >= DE.d.degree(DE.t):
        m = p.degree(DE.t) - DE.d.degree(DE.t) + 1
        q0 = Poly(DE.t**m, DE.t).mul(Poly(p.as_poly(DE.t).LC()/
            (m*DE.d.LC()), DE.t))
        q += q0
        p = p - derivation(q0, DE)

    return (q, p)

