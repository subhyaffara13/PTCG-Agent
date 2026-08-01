
def quo_z(p, q, x):
    """
    Intended mainly for p, q polynomials in Z[x] so that,
    on dividing p by q, the quotient will also be in Z[x]. (However,
    it also works fine for polynomials in Q[x].) It is assumed
    that degree(p, x) >= degree(q, x).

    It premultiplies p by the _absolute_ value of the leading coefficient
    of q, raised to the power deg(p) - deg(q) + 1 and then performs
    polynomial division in Q[x], using the function quo(p, q, x).

    By contrast the function pquo(p, q, x) does _not_ use the absolute
    value of the leading coefficient of q.

    See also function rem_z(p, q, x) for additional comments and references.

    """
    if (p.as_poly().is_univariate and q.as_poly().is_univariate and
            p.as_poly().gens == q.as_poly().gens):
        delta = (degree(p, x) - degree(q, x) + 1)
        return quo(Abs(LC(q, x))**delta  *  p, q, x)
    else:
        return pquo(p, q, x)

