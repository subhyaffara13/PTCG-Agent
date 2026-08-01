
def integrate_hypertangent_polynomial(p, DE):
    """
    Integration of hypertangent polynomials.

    Explanation
    ===========

    Given a differential field k such that sqrt(-1) is not in k, a
    hypertangent monomial t over k, and p in k[t], return q in k[t] and
    c in k such that p - Dq - c*D(t**2 + 1)/(t**1 + 1) is in k and p -
    Dq does not have an elementary integral over k(t) if Dc != 0.
    """
    # XXX: Make sure that sqrt(-1) is not in k.
    q, r = polynomial_reduce(p, DE)
    a = DE.d.exquo(Poly(DE.t**2 + 1, DE.t))
    c = Poly(r.nth(1)/(2*a.as_expr()), DE.t)
    return (q, c)

