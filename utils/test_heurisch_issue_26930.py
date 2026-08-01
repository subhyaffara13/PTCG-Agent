
def test_heurisch_issue_26930():
    integrand = x**Rational(4, 3)*log(x)
    anti = 3*x**(S(7)/3)*log(x)/7 - 9*x**(S(7)/3)/49
    assert heurisch(integrand, x) == anti
    assert integrate(integrand, x) == anti
    assert integrate(integrand, (x, 0, 1)) == -S(9)/49

