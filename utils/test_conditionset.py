
def test_conditionset():
    assert solveset(Eq(sin(x)**2 + cos(x)**2, 1), x, domain=S.Reals
        ) is S.Reals

    assert solveset(Eq(x**2 + x*sin(x), 1), x, domain=S.Reals
        ).dummy_eq(ConditionSet(x, Eq(x**2 + x*sin(x) - 1, 0), S.Reals))

    assert dumeq(solveset(Eq(-I*(exp(I*x) - exp(-I*x))/2, 1), x
        ), imageset(Lambda(n, 2*n*pi + pi/2), S.Integers))

    assert solveset(x + sin(x) > 1, x, domain=S.Reals
        ).dummy_eq(ConditionSet(x, x + sin(x) > 1, S.Reals))

    assert solveset(Eq(sin(Abs(x)), x), x, domain=S.Reals
        ).dummy_eq(ConditionSet(x, Eq(-x + sin(Abs(x)), 0), S.Reals))

    assert solveset(y**x-z, x, S.Reals
        ).dummy_eq(ConditionSet(x, Eq(y**x - z, 0), S.Reals))

