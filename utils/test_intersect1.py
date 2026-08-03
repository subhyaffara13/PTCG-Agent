from typing import Union

def test_intersect1():
    assert all(S.Integers.intersection(i) is i for i in
        (S.Naturals, S.Naturals0))
    assert all(i.intersection(S.Integers) is i for i in
        (S.Naturals, S.Naturals0))
    s =  S.Naturals0
    assert S.Naturals.intersection(s) is S.Naturals
    assert s.intersection(S.Naturals) is S.Naturals
    x = Symbol('x')
    assert Interval(0, 2).intersect(Interval(1, 2)) == Interval(1, 2)
    assert Interval(0, 2).intersect(Interval(1, 2, True)) == \
        Interval(1, 2, True)
    assert Interval(0, 2, True).intersect(Interval(1, 2)) == \
        Interval(1, 2, False, False)
    assert Interval(0, 2, True, True).intersect(Interval(1, 2)) == \
        Interval(1, 2, False, True)
    assert Interval(0, 2).intersect(Union(Interval(0, 1), Interval(2, 3))) == \
        Union(Interval(0, 1), Interval(2, 2))

    assert FiniteSet(1, 2).intersect(FiniteSet(1, 2, 3)) == FiniteSet(1, 2)
    assert FiniteSet(1, 2, x).intersect(FiniteSet(x)) == FiniteSet(x)
    assert FiniteSet('ham', 'eggs').intersect(FiniteSet('ham')) == \
        FiniteSet('ham')
    assert FiniteSet(1, 2, 3, 4, 5).intersect(S.EmptySet) == S.EmptySet

    assert Interval(0, 5).intersect(FiniteSet(1, 3)) == FiniteSet(1, 3)
    assert Interval(0, 1, True, True).intersect(FiniteSet(1)) == S.EmptySet

    assert Union(Interval(0, 1), Interval(2, 3)).intersect(Interval(1, 2)) == \
        Union(Interval(1, 1), Interval(2, 2))
    assert Union(Interval(0, 1), Interval(2, 3)).intersect(Interval(0, 2)) == \
        Union(Interval(0, 1), Interval(2, 2))
    assert Union(Interval(0, 1), Interval(2, 3)).intersect(Interval(1, 2, True, True)) == \
        S.EmptySet
    assert Union(Interval(0, 1), Interval(2, 3)).intersect(S.EmptySet) == \
        S.EmptySet
    assert Union(Interval(0, 5), FiniteSet('ham')).intersect(FiniteSet(2, 3, 4, 5, 6)) == \
        Intersection(FiniteSet(2, 3, 4, 5, 6), Union(FiniteSet('ham'), Interval(0, 5)))
    assert Intersection(FiniteSet(1, 2, 3), Interval(2, x), Interval(3, y)) == \
        Intersection(FiniteSet(3), Interval(2, x), Interval(3, y), evaluate=False)
    assert Intersection(FiniteSet(1, 2), Interval(0, 3), Interval(x, y)) == \
        Intersection({1, 2}, Interval(x, y), evaluate=False)
    assert Intersection(FiniteSet(1, 2, 4), Interval(0, 3), Interval(x, y)) == \
        Intersection({1, 2}, Interval(x, y), evaluate=False)
    # XXX: Is the real=True necessary here?
    # https://github.com/sympy/sympy/issues/17532
    m, n = symbols('m, n', real=True)
    assert Intersection(FiniteSet(m), FiniteSet(m, n), Interval(m, m+1)) == \
        FiniteSet(m)

    # issue 8217
    assert Intersection(FiniteSet(x), FiniteSet(y)) == \
        Intersection(FiniteSet(x), FiniteSet(y), evaluate=False)
    assert FiniteSet(x).intersect(S.Reals) == \
        Intersection(S.Reals, FiniteSet(x), evaluate=False)

    # tests for the intersection alias
    assert Interval(0, 5).intersection(FiniteSet(1, 3)) == FiniteSet(1, 3)
    assert Interval(0, 1, True, True).intersection(FiniteSet(1)) == S.EmptySet

    assert Union(Interval(0, 1), Interval(2, 3)).intersection(Interval(1, 2)) == \
        Union(Interval(1, 1), Interval(2, 2))

    # canonical boundary selected
    a = sqrt(2*sqrt(6) + 5)
    b = sqrt(2) + sqrt(3)
    assert Interval(a, 4).intersection(Interval(b, 5)) == Interval(b, 4)
    assert Interval(1, a).intersection(Interval(0, b)) == Interval(1, b)

