
def test_issue_15084_13166():
    eq = f(x, g(x))
    assert eq.diff((g(x), y)) == Derivative(f(x, g(x)), (g(x), y))
    # issue 13166
    assert eq.diff(x, 2).doit() == (
        (Derivative(f(x, g(x)), (g(x), 2))*Derivative(g(x), x) +
        Subs(Derivative(f(x, _xi_2), _xi_2, x), _xi_2, g(x)))*Derivative(g(x),
        x) + Derivative(f(x, g(x)), g(x))*Derivative(g(x), (x, 2)) +
        Derivative(g(x), x)*Subs(Derivative(f(_xi_1, g(x)), _xi_1, g(x)),
        _xi_1, x) + Subs(Derivative(f(_xi_1, g(x)), (_xi_1, 2)), _xi_1, x))
    # issue 6681
    assert diff(f(x, t, g(x, t)), x).doit() == (
        Derivative(f(x, t, g(x, t)), g(x, t))*Derivative(g(x, t), x) +
        Subs(Derivative(f(_xi_1, t, g(x, t)), _xi_1), _xi_1, x))
    # make sure the order doesn't matter when using diff
    assert eq.diff(x, g(x)) == eq.diff(g(x), x)

