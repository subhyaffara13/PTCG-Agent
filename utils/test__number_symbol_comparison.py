
def test_NumberSymbol_comparison():
    from sympy.core.tests.test_relational import rel_check
    rpi = Rational('905502432259640373/288230376151711744')
    fpi = Float(float(pi))
    assert rel_check(rpi, fpi)

