
def test_union_contains():
    x = Symbol('x')
    i1 = Interval(0, 1)
    i2 = Interval(2, 3)
    i3 = Union(i1, i2)
    assert i3.as_relational(x) == Or(And(S.Zero <= x, x <= 1), And(S(2) <= x, x <= 3))
    raises(TypeError, lambda: x in i3)
    e = i3.contains(x)
    assert e == i3.as_relational(x)
    assert e.subs(x, -0.5) is false
    assert e.subs(x, 0.5) is true
    assert e.subs(x, 1.5) is false
    assert e.subs(x, 2.5) is true
    assert e.subs(x, 3.5) is false

    U = Interval(0, 2, True, True) + Interval(10, oo) + FiniteSet(-1, 2, 5, 6)
    assert all(el not in U for el in [0, 4, -oo])
    assert all(el in U for el in [2, 5, 10])

