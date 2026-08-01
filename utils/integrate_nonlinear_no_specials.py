
def integrate_nonlinear_no_specials(a, d, DE, z=None):
    """
    Integration of nonlinear monomials with no specials.

    Explanation
    ===========

    Given a nonlinear monomial t over k such that Sirr ({p in k[t] | p is
    special, monic, and irreducible}) is empty, and f in k(t), returns g
    elementary over k(t) and a Boolean b in {True, False} such that f - Dg is
    in k if b == True, or f - Dg does not have an elementary integral over k(t)
    if b == False.

    This function is applicable to all nonlinear extensions, but in the case
    where it returns b == False, it will only have proven that the integral of
    f - Dg is nonelementary if Sirr is empty.

    This function returns a Basic expression.
    """
    # TODO: Integral from k?
    # TODO: split out nonelementary integral
    # XXX: a and d must be canceled, or this might not return correct results
    z = z or Dummy("z")
    s = list(zip(reversed(DE.T), reversed([f(DE.x) for f in DE.Tfuncs])))

    g1, h, r = hermite_reduce(a, d, DE)
    g2, b = residue_reduce(h[0], h[1], DE, z=z)
    if not b:
        return ((g1[0].as_expr()/g1[1].as_expr()).subs(s) +
            residue_reduce_to_basic(g2, DE, z), b)

    # Because f has no specials, this should be a polynomial in t, or else
    # there is a bug.
    p = cancel(h[0].as_expr()/h[1].as_expr() - residue_reduce_derivation(g2,
        DE, z).as_expr() + r[0].as_expr()/r[1].as_expr()).as_poly(DE.t)
    q1, q2 = polynomial_reduce(p, DE)

    if q2.expr.has(DE.t):
        b = False
    else:
        b = True

    ret = (cancel(g1[0].as_expr()/g1[1].as_expr() + q1.as_expr()).subs(s) +
        residue_reduce_to_basic(g2, DE, z))
    return (ret, b)

