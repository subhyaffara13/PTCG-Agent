
def field_isomorphism_factor(a, b):
    """Construct field isomorphism via factorization. """
    _, factors = factor_list(a.minpoly, extension=b)
    for f, _ in factors:
        if f.degree() == 1:
            # Any linear factor f(x) represents some conjugate of a in QQ(b).
            # We want to know whether this linear factor represents a itself.
            # Let f = x - c
            c = -f.rep.TC()
            # Write c as polynomial in b
            coeffs = c.to_sympy_list()
            d, terms = len(coeffs) - 1, []
            for i, coeff in enumerate(coeffs):
                terms.append(coeff*b.root**(d - i))
            r = Add(*terms)
            # Check whether we got the number a
            if a.minpoly.same_root(r, a):
                return coeffs

    # If none of the linear factors represented a in QQ(b), then in fact a is
    # not an element of QQ(b).
    return None

