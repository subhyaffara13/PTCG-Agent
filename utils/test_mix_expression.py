
def test_mix_expression():
    Y, E = Poisson('Y', 1), Exponential('E', 1)
    k = Dummy('k')
    expr1 = Integral(Sum(exp(-1)*Integral(exp(-k)*DiracDelta(k - 2), (k, 0, oo)
    )/factorial(k), (k, 0, oo)), (k, -oo, 0))
    expr2 = Integral(Sum(exp(-1)*Integral(exp(-k)*DiracDelta(k - 2), (k, 0, oo)
    )/factorial(k), (k, 0, oo)), (k, 0, oo))
    assert P(Eq(Y + E, 1)) == 0
    assert P(Ne(Y + E, 2)) == 1
    with ignore_warnings(UserWarning): ### TODO: Restore tests once warnings are removed
        assert P(E + Y < 2, evaluate=False).rewrite(Integral).dummy_eq(expr1)
        assert P(E + Y > 2, evaluate=False).rewrite(Integral).dummy_eq(expr2)

