from typing import Union

def test_solve_abs():
    n = Dummy('n')
    raises(ValueError, lambda: solveset(Abs(x) - 1, x))
    assert solveset(Abs(x) - n, x, S.Reals).dummy_eq(
        ConditionSet(x, Contains(n, Interval(0, oo)), {-n, n}))
    assert solveset_real(Abs(x) - 2, x) == FiniteSet(-2, 2)
    assert solveset_real(Abs(x) + 2, x) is S.EmptySet
    assert solveset_real(Abs(x + 3) - 2*Abs(x - 3), x) == \
        FiniteSet(1, 9)
    assert solveset_real(2*Abs(x) - Abs(x - 1), x) == \
        FiniteSet(-1, Rational(1, 3))

    sol = ConditionSet(
            x,
            And(
                Contains(b, Interval(0, oo)),
                Contains(a + b, Interval(0, oo)),
                Contains(a - b, Interval(0, oo))),
            FiniteSet(-a - b - 3, -a + b - 3, a - b - 3, a + b - 3))
    eq = Abs(Abs(x + 3) - a) - b
    assert invert_real(eq, 0, x)[1] == sol
    reps = {a: 3, b: 1}
    eqab = eq.subs(reps)
    for si in sol.subs(reps):
        assert not eqab.subs(x, si)
    assert dumeq(solveset(Eq(sin(Abs(x)), 1), x, domain=S.Reals), Union(
        Intersection(Interval(0, oo), Union(
        Intersection(ImageSet(Lambda(n, 2*n*pi + 3*pi/2), S.Integers),
            Interval(-oo, 0)),
        Intersection(ImageSet(Lambda(n, 2*n*pi + pi/2), S.Integers),
            Interval(0, oo))))))

