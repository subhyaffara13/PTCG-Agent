
def test_issue_4890():
    z = Symbol('z', positive=True)
    assert integrate(exp(-log(x)**2), x) == \
        sqrt(pi)*exp(Rational(1, 4))*erf(log(x) - S.Half)/2
    assert integrate(exp(log(x)**2), x) == \
        sqrt(pi)*exp(Rational(-1, 4))*erfi(log(x)+S.Half)/2
    assert integrate(exp(-z*log(x)**2), x) == \
        sqrt(pi)*exp(1/(4*z))*erf(sqrt(z)*log(x) - 1/(2*sqrt(z)))/(2*sqrt(z))

