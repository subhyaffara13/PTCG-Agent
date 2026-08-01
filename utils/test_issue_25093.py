
def test_issue_25093():
    ap = Symbol('ap', positive=True)
    an = Symbol('an', negative=True)
    assert manualintegrate(exp(a*x**2 + b), x) == sqrt(pi)*exp(b)*erfi(sqrt(a)*x)/(2*sqrt(a))
    assert manualintegrate(exp(ap*x**2 + b), x) == sqrt(pi)*exp(b)*erfi(sqrt(ap)*x)/(2*sqrt(ap))
    assert manualintegrate(exp(an*x**2 + b), x) == -sqrt(pi)*exp(b)*erf(an*x/sqrt(-an))/(2*sqrt(-an))
    assert manualintegrate(sin(a*x**2 + b), x) == (
        sqrt(2)*sqrt(pi)*(sin(b)*fresnelc(sqrt(2)*sqrt(a)*x/sqrt(pi))
        + cos(b)*fresnels(sqrt(2)*sqrt(a)*x/sqrt(pi)))/(2*sqrt(a)))
    assert manualintegrate(cos(a*x**2 + b), x) == (
        sqrt(2)*sqrt(pi)*(-sin(b)*fresnels(sqrt(2)*sqrt(a)*x/sqrt(pi))
        + cos(b)*fresnelc(sqrt(2)*sqrt(a)*x/sqrt(pi)))/(2*sqrt(a)))

