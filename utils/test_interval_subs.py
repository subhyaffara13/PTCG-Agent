
def test_interval_subs():
    a = Symbol('a', real=True)

    assert Interval(0, a).subs(a, 2) == Interval(0, 2)
    assert Interval(a, 0).subs(a, 2) == S.EmptySet

