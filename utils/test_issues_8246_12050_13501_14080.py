
def test_issues_8246_12050_13501_14080():
    a = symbols('a', nonzero=True)
    assert integrate(a/(x**2 + a**2), x) == atan(x/a)
    assert integrate(1/(x**2 + a**2), x) == atan(x/a)/a
    assert integrate(1/(1 + a**2*x**2), x) == atan(a*x)/a

