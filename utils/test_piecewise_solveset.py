
def test_piecewise_solveset():
    eq = Piecewise((x - 2, Gt(x, 2)), (2 - x, True)) - 3
    assert set(solveset_real(eq, x)) == set(FiniteSet(-1, 5))

    absxm3 = Piecewise(
        (x - 3, 0 <= x - 3),
        (3 - x, 0 > x - 3))
    y = Symbol('y', positive=True)
    assert solveset_real(absxm3 - y, x) == FiniteSet(-y + 3, y + 3)

    f = Piecewise(((x - 2)**2, x >= 0), (0, True))
    assert solveset(f, x, domain=S.Reals) == Union(FiniteSet(2), Interval(-oo, 0, True, True))

    assert solveset(
        Piecewise((x + 1, x > 0), (I, True)) - I, x, S.Reals
        ) == Interval(-oo, 0)

    assert solveset(Piecewise((x - 1, Ne(x, I)), (x, True)), x) == FiniteSet(1)

    # issue 19718
    g = Piecewise((1, x > 10), (0, True))
    assert solveset(g > 0, x, S.Reals) == Interval.open(10, oo)

    from sympy.logic.boolalg import BooleanTrue
    f = BooleanTrue()
    assert solveset(f, x, domain=Interval(-3, 10)) == Interval(-3, 10)

    # issue 20552
    f = Piecewise((0, Eq(x, 0)), (x**2/Abs(x), True))
    g = Piecewise((0, Eq(x, pi)), ((x - pi)/sin(x), True))
    assert solveset(f, x, domain=S.Reals) == FiniteSet(0)
    assert solveset(g) == FiniteSet(pi)

