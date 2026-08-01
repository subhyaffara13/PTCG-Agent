
def test_issue_20985():
    from sympy.core.symbol import symbols
    w, R = symbols('w R')
    poly = Poly(1.0 + I*w/R, w, 1/R)
    assert poly.degree() == S(1)

