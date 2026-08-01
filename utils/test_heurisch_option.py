
def test_heurisch_option():
    raises(ValueError, lambda: integrate(1/x, x, risch=True, heurisch=True))
    # an integral that heurisch can handle
    assert integrate(exp(x**2), x, heurisch=True) == sqrt(pi)*erfi(x)/2
    # an integral that heurisch currently cannot handle
    assert integrate(exp(x)/x, x, heurisch=True) == Integral(exp(x)/x, x)
    # an integral where heurisch currently hangs, issue 15471
    assert integrate(log(x)*cos(log(x))/x**Rational(3, 4), x, heurisch=False) == (
        -128*x**Rational(1, 4)*sin(log(x))/289 + 240*x**Rational(1, 4)*cos(log(x))/289 +
        (16*x**Rational(1, 4)*sin(log(x))/17 + 4*x**Rational(1, 4)*cos(log(x))/17)*log(x))

