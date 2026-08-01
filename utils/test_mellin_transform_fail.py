
def test_mellin_transform_fail():
    skip("Risch takes forever.")

    MT = mellin_transform

    bpos = symbols('b', positive=True)
    # bneg = symbols('b', negative=True)

    expr = (sqrt(x + b**2) + b)**a/sqrt(x + b**2)
    # TODO does not work with bneg, argument wrong. Needs changes to matching.
    assert MT(expr.subs(b, -bpos), x, s) == \
        ((-1)**(a + 1)*2**(a + 2*s)*bpos**(a + 2*s - 1)*gamma(a + s)
         *gamma(1 - a - 2*s)/gamma(1 - s),
            (-re(a), -re(a)/2 + S.Half), True)

    expr = (sqrt(x + b**2) + b)**a
    assert MT(expr.subs(b, -bpos), x, s) == \
        (
            2**(a + 2*s)*a*bpos**(a + 2*s)*gamma(-a - 2*
                   s)*gamma(a + s)/gamma(-s + 1),
            (-re(a), -re(a)/2), True)

    # Test exponent 1:
    assert MT(expr.subs({b: -bpos, a: 1}), x, s) == \
        (-bpos**(2*s + 1)*gamma(s)*gamma(-s - S.Half)/(2*sqrt(pi)),
            (-1, Rational(-1, 2)), True)

