
def test_issue_9623():
    n = Symbol('n')

    a = S.Reals
    b = Interval(0, oo)
    c = FiniteSet(n)

    assert Intersection(a, b, c) == Intersection(b, c)
    assert Intersection(Interval(1, 2), Interval(3, 4), FiniteSet(n)) == EmptySet

