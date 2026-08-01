
def test_has_reversed_limits():
    assert Sum(1, (x, 1, 1)).has_reversed_limits is False
    assert Sum(1, (x, 1, 9)).has_reversed_limits is False
    assert Sum(1, (x, 1, -9)).has_reversed_limits is True
    assert Sum(1, (x, 1, 0)).has_reversed_limits is True
    assert Sum(1, (x, 1, oo)).has_reversed_limits is False
    M = Symbol('M')
    assert Sum(1, (x, 1, M)).has_reversed_limits is None
    M = Symbol('M', positive=True, integer=True)
    assert Sum(1, (x, 1, M)).has_reversed_limits is False
    assert Sum(1, (x, 1, M), (y, -oo, oo)).has_reversed_limits is False
    M = Symbol('M', negative=True)
    assert Sum(1, (x, 1, M)).has_reversed_limits is True

    assert Sum(1, (x, 1, M), (y, -oo, oo)).has_reversed_limits is True
    assert Sum(1, (x, oo, oo)).has_reversed_limits is None

