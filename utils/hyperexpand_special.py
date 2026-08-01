
def hyperexpand_special(ap, bq, z):
    """
    Try to find a closed-form expression for hyper(ap, bq, z), where ``z``
    is supposed to be a "special" value, e.g. 1.

    This function tries various of the classical summation formulae
    (Gauss, Saalschuetz, etc).
    """
    # This code is very ad-hoc. There are many clever algorithms
    # (notably Zeilberger's) related to this problem.
    # For now we just want a few simple cases to work.
    p, q = len(ap), len(bq)
    z_ = z
    z = unpolarify(z)
    if z == 0:
        return S.One
    from sympy.simplify.simplify import simplify
    if p == 2 and q == 1:
        # 2F1
        a, b, c = ap + bq
        if z == 1:
            # Gauss
            return gamma(c - a - b)*gamma(c)/gamma(c - a)/gamma(c - b)
        if z == -1 and simplify(b - a + c) == 1:
            b, a = a, b
        if z == -1 and simplify(a - b + c) == 1:
            # Kummer
            if b.is_integer and b.is_negative:
                return 2*cos(pi*b/2)*gamma(-b)*gamma(b - a + 1) \
                    /gamma(-b/2)/gamma(b/2 - a + 1)
            else:
                return gamma(b/2 + 1)*gamma(b - a + 1) \
                    /gamma(b + 1)/gamma(b/2 - a + 1)
    # TODO tons of more formulae
    #      investigate what algorithms exist
    return hyper(ap, bq, z_)

