
def test_has_finite_limits():
    x = Symbol('x')
    assert Sum(1, (x, 1, 9)).has_finite_limits is True
    assert Sum(1, (x, 1, oo)).has_finite_limits is False
    M = Symbol('M')
    assert Sum(1, (x, 1, M)).has_finite_limits is None
    M = Symbol('M', positive=True)
    assert Sum(1, (x, 1, M)).has_finite_limits is True
    x = Symbol('x', positive=True)
    M = Symbol('M')
    assert Sum(1, (x, 1, M)).has_finite_limits is True

    assert Sum(1, (x, 1, M), (y, -oo, oo)).has_finite_limits is False

