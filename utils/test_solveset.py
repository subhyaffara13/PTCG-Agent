
def test_solveset():
    f = Function('f')
    raises(ValueError, lambda: solveset(x + y))
    assert solveset(x, 1) == S.EmptySet
    assert solveset(f(1)**2 + y + 1, f(1)
        ) == FiniteSet(-sqrt(-y - 1), sqrt(-y - 1))
    assert solveset(f(1)**2 - 1, f(1), S.Reals) == FiniteSet(-1, 1)
    assert solveset(f(1)**2 + 1, f(1)) == FiniteSet(-I, I)
    assert solveset(x - 1, 1) == FiniteSet(x)
    assert solveset(sin(x) - cos(x), sin(x)) == FiniteSet(cos(x))

    assert solveset(0, domain=S.Reals) == S.Reals
    assert solveset(1) == S.EmptySet
    assert solveset(True, domain=S.Reals) == S.Reals  # issue 10197
    assert solveset(False, domain=S.Reals) == S.EmptySet

    assert solveset(exp(x) - 1, domain=S.Reals) == FiniteSet(0)
    assert solveset(exp(x) - 1, x, S.Reals) == FiniteSet(0)
    assert solveset(Eq(exp(x), 1), x, S.Reals) == FiniteSet(0)
    assert solveset(exp(x) - 1, exp(x), S.Reals) == FiniteSet(1)
    A = Indexed('A', x)
    assert solveset(A - 1, A, S.Reals) == FiniteSet(1)

    assert solveset(x - 1 >= 0, x, S.Reals) == Interval(1, oo)
    assert solveset(exp(x) - 1 >= 0, x, S.Reals) == Interval(0, oo)

    assert dumeq(solveset(exp(x) - 1, x), imageset(Lambda(n, 2*I*pi*n), S.Integers))
    assert dumeq(solveset(Eq(exp(x), 1), x), imageset(Lambda(n, 2*I*pi*n),
                                                  S.Integers))
    # issue 13825
    assert solveset(x**2 + f(0) + 1, x) == {-sqrt(-f(0) - 1), sqrt(-f(0) - 1)}

    # issue 19977
    assert solveset(atan(log(x)) > 0, x, domain=Interval.open(0, oo)) == Interval.open(1, oo)

