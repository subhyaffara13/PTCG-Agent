
def test_issue_17898():
    if not scipy:
        skip("scipy not installed")
    x = symbols("x")
    f_ = lambdify([x], sympy.LambertW(x,-1), modules='scipy')
    assert f_(0.1) == mpmath.lambertw(0.1, -1)

