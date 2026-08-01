
def test_equal():
    b = Symbol("b")
    a = Symbol("a")
    e1 = a + b
    e2 = 2*a*b
    e3 = a**3*b**2
    e4 = a*b + b*a
    assert not e1 == e2
    assert not e1 == e2
    assert e1 != e2
    assert e2 == e4
    assert e2 != e3
    assert not e2 == e3

    x = Symbol("x")
    e1 = exp(x + 1/x)
    y = Symbol("x")
    e2 = exp(y + 1/y)
    assert e1 == e2
    assert not e1 != e2
    y = Symbol("y")
    e2 = exp(y + 1/y)
    assert not e1 == e2
    assert e1 != e2

    e5 = Rational(3) + 2*x - x - x
    assert e5 == 3
    assert 3 == e5
    assert e5 != 4
    assert 4 != e5
    assert e5 != 3 + x
    assert 3 + x != e5


def test_equal():
    """Test for equality"""
    assert Q.positive(x) == Q.positive(x)
    assert Q.positive(x) != ~Q.positive(x)
    assert ~Q.positive(x) == ~Q.positive(x)


def test_equal(dtype, fill_value):
    a = SparseDtype(dtype, fill_value)
    b = SparseDtype(dtype, fill_value)
    assert a == b
    assert b == a


def test_equal(Poly):
    p1 = Poly([1, 2, 3], domain=[0, 1], window=[2, 3])
    p2 = Poly([1, 1, 1], domain=[0, 1], window=[2, 3])
    p3 = Poly([1, 2, 3], domain=[1, 2], window=[2, 3])
    p4 = Poly([1, 2, 3], domain=[0, 1], window=[1, 2])
    assert_(p1 == p1)
    assert_(not p1 == p2)
    assert_(not p1 == p3)
    assert_(not p1 == p4)


def test_equal():
    gs = gridspec.GridSpec(2, 1)
    assert gs[0, 0] == gs[0, 0]
    assert gs[:, 0] == gs[:, 0]

