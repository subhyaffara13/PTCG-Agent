
def test_rewrite_trigh():
    # if this import passes then the test below should also pass
    from sympy.functions.elementary.hyperbolic import sech
    assert solve(sinh(x) + sech(x)) == [
        2*atanh(Rational(-1, 2) + sqrt(5)/2 - sqrt(-2*sqrt(5) + 2)/2),
        2*atanh(Rational(-1, 2) + sqrt(5)/2 + sqrt(-2*sqrt(5) + 2)/2),
        2*atanh(-sqrt(5)/2 - S.Half + sqrt(2 + 2*sqrt(5))/2),
        2*atanh(-sqrt(2 + 2*sqrt(5))/2 - sqrt(5)/2 - S.Half)]

