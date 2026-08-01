
def test_issue_4212_real():
    xr = symbols('xr', real=True)
    negabsx = Piecewise((-xr, xr < 0), (xr, True))
    assert integrate(sign(xr), xr) == negabsx

