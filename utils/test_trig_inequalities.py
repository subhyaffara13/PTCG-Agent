from typing import Union

def test_trig_inequalities():
    # all the inequalities are solved in a periodic interval.
    assert isolve(sin(x) < S.Half, x, relational=False) == \
        Union(Interval(0, pi/6, False, True), Interval.open(pi*Rational(5, 6), 2*pi))
    assert isolve(sin(x) > S.Half, x, relational=False) == \
        Interval(pi/6, pi*Rational(5, 6), True, True)
    assert isolve(cos(x) < S.Zero, x, relational=False) == \
        Interval(pi/2, pi*Rational(3, 2), True, True)
    assert isolve(cos(x) >= S.Zero, x, relational=False) == \
        Union(Interval(0, pi/2), Interval.Ropen(pi*Rational(3, 2), 2*pi))

    assert isolve(tan(x) < S.One, x, relational=False) == \
        Union(Interval.Ropen(0, pi/4), Interval.open(pi/2, pi))

    assert isolve(sin(x) <= S.Zero, x, relational=False) == \
        Union(FiniteSet(S.Zero), Interval.Ropen(pi, 2*pi))

    assert isolve(sin(x) <= S.One, x, relational=False) == S.Reals
    assert isolve(cos(x) < S(-2), x, relational=False) == S.EmptySet
    assert isolve(sin(x) >= S.NegativeOne, x, relational=False) == S.Reals
    assert isolve(cos(x) > S.One, x, relational=False) == S.EmptySet

