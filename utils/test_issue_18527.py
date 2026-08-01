
def test_issue_18527():
    # The manual integrator can not currently solve this. Assert that it does
    # not give an incorrect result involving Abs when x has real assumptions.
    xr = symbols('xr', real=True)
    expr = (cos(x)/(4+(sin(x))**2))
    res_real = integrate(expr.subs(x, xr), xr, manual=True).subs(xr, x)
    assert integrate(expr, x, manual=True) == res_real == Integral(expr, x)

