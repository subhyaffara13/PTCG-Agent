
def _complete_the_square_in_denom(f, s):
    from sympy.simplify.radsimp import fraction
    [n, d] = fraction(f)
    if d.is_polynomial(s):
        cf = d.as_poly(s).all_coeffs()
        if len(cf) == 3:
            a, b, c = cf
            d = a*((s+b/(2*a))**2+c/a-(b/(2*a))**2)
    return n/d

