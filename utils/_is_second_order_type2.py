
def _is_second_order_type2(A, t):
    term = _factor_matrix(A, t)
    is_type2 = False

    if term is not None:
        term = 1/term[0]
        is_type2 = term.is_polynomial()

    if is_type2:
        poly = Poly(term.expand(), t)
        monoms = poly.monoms()

        if monoms[0][0] in (2, 4):
            cs = _get_poly_coeffs(poly, 4)
            a, b, c, d, e = cs

            a1 = powdenest(sqrt(a), force=True)
            c1 = powdenest(sqrt(e), force=True)
            b1 = powdenest(sqrt(c - 2*a1*c1), force=True)

            is_type2 = (b == 2*a1*b1) and (d == 2*b1*c1)
            term = a1*t**2 + b1*t + c1

        else:
            is_type2 = False

    return is_type2, term

