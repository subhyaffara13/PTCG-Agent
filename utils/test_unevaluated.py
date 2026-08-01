
def test_unevaluated():
    X = Normal('x', 0, 1)
    k = Dummy('k')
    expr1 = Integral(sqrt(2)*k*exp(-k**2/2)/(2*sqrt(pi)), (k, -oo, oo))
    expr2 = Integral(sqrt(2)*exp(-k**2/2)/(2*sqrt(pi)), (k, 0, oo))
    with ignore_warnings(UserWarning): ### TODO: Restore tests once warnings are removed
        assert E(X, evaluate=False).rewrite(Integral).dummy_eq(expr1)
        assert E(X + 1, evaluate=False).rewrite(Integral).dummy_eq(expr1 + 1)
        assert P(X > 0, evaluate=False).rewrite(Integral).dummy_eq(expr2)

    assert P(X > 0, X**2 < 1) == S.Half


def test_unevaluated():
    """Check that evaluate=False returns unevaluated Dagger.
    """
    x = symbols("x", real=True)
    assert Dagger(x) == x
    result = Dagger(x, evaluate=False)
    assert result.args == (x,) and isinstance(result, adjoint)

