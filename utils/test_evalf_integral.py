
def test_evalf_integral():
    # test that workprec has to increase in order to get a result other than 0
    eps = Rational(1, 1000000)
    assert Integral(sin(x), (x, -pi, pi + eps)).n(2)._prec == 10

