
def test_unevaluated_integrals():
    f = Function('f')
    p = Piecewise((1, Eq(f(x) - 1, 0)), (2, x - 10 < 0), (0, True))
    assert p.integrate(x) == Integral(p, x)
    assert p.integrate((x, 0, 5)) == Integral(p, (x, 0, 5))
    # test it by replacing f(x) with x%2 which will not
    # affect the answer: the integrand is essentially 2 over
    # the domain of integration
    assert Integral(p, (x, 0, 5)).subs(f(x), x%2).n() == 10.0

    # this is a test of using _solve_inequality when
    # solve_univariate_inequality fails
    assert p.integrate(y) == Piecewise(
        (y, Eq(f(x), 1) | ((x < 10) & Eq(f(x), 1))),
        (2*y, (x > -oo) & (x < 10)), (0, True))

