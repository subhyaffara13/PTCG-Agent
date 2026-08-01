
def test_issue_9637():
    n = Symbol('n')
    a = FiniteSet(n)
    b = FiniteSet(2, n)
    assert Complement(S.Reals, a) == Complement(S.Reals, a, evaluate=False)
    assert Complement(Interval(1, 3), a) == Complement(Interval(1, 3), a, evaluate=False)
    assert Complement(Interval(1, 3), b) == \
        Complement(Union(Interval(1, 2, False, True), Interval(2, 3, True, False)), a)
    assert Complement(a, S.Reals) == Complement(a, S.Reals, evaluate=False)
    assert Complement(a, Interval(1, 3)) == Complement(a, Interval(1, 3), evaluate=False)

