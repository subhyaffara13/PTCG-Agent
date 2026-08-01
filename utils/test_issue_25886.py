
def test_issue_25886():
    # https://github.com/sympy/sympy/issues/25886
    f = (1-x)*exp(0.937098661j*x)
    F_exp = (1.0*(-1.0671234968289*I*y
             + 1.13875255748434
             + 1.0671234968289*I)*exp(0.937098661*I*y)
            - 1.13875255748434*exp(0.937098661*I))
    F = integrate(f, (x, y, 1.0))
    assert F.is_same(F_exp, math.isclose)

