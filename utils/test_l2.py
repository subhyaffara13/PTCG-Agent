
def test_L2():
    assert sqrt(999983) - (999983**3)**R(1, 6) == 0


def test_L2():
    b1 = L2(Interval(-oo, 1))
    assert isinstance(b1, L2)
    assert b1.dimension is oo
    assert b1.interval == Interval(-oo, 1)

    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    b2 = L2(Interval(x, y))
    assert b2.dimension is oo
    assert b2.interval == Interval(x, y)
    assert b2.subs(x, -1) == L2(Interval(-1, y))

