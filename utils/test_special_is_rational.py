
def test_special_is_rational():
    i = Symbol('i', integer=True)
    i2 = Symbol('i2', integer=True)
    ni = Symbol('ni', integer=True, nonzero=True)
    r = Symbol('r', rational=True)
    rn = Symbol('r', rational=True, nonzero=True)
    nr = Symbol('nr', irrational=True)
    x = Symbol('x')
    assert sqrt(3).is_rational is False
    assert (3 + sqrt(3)).is_rational is False
    assert (3*sqrt(3)).is_rational is False
    assert exp(3).is_rational is False
    assert exp(ni).is_rational is False
    assert exp(rn).is_rational is False
    assert exp(x).is_rational is None
    assert exp(log(3), evaluate=False).is_rational is True
    assert log(exp(3), evaluate=False).is_rational is True
    assert log(3).is_rational is False
    assert log(ni + 1).is_rational is False
    assert log(rn + 1).is_rational is False
    assert log(x).is_rational is None
    assert (sqrt(3) + sqrt(5)).is_rational is None
    assert (sqrt(3) + S.Pi).is_rational is False
    assert (x**i).is_rational is None
    assert (i**i).is_rational is True
    assert (i**i2).is_rational is None
    assert (r**i).is_rational is None
    assert (r**r).is_rational is None
    assert (r**x).is_rational is None
    assert (nr**i).is_rational is None  # issue 8598
    assert (nr**Symbol('z', zero=True)).is_rational
    assert sin(1).is_rational is False
    assert sin(ni).is_rational is False
    assert sin(rn).is_rational is False
    assert sin(x).is_rational is None
    assert asin(r).is_rational is False
    assert sin(asin(3), evaluate=False).is_rational is True

