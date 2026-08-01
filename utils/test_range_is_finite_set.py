
def test_range_is_finite_set():
    assert Range(-100, 100).is_finite_set is True
    assert Range(2, oo).is_finite_set is False
    assert Range(-oo, 50).is_finite_set is False
    assert Range(-oo, oo).is_finite_set is False
    assert Range(oo, -oo).is_finite_set is True
    assert Range(0, 0).is_finite_set is True
    assert Range(oo, oo).is_finite_set is True
    assert Range(-oo, -oo).is_finite_set is True
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    assert Range(n, n + 49).is_finite_set is True
    assert Range(n, 0).is_finite_set is True
    assert Range(-3, n + 7).is_finite_set is True
    assert Range(n, m).is_finite_set is True
    assert Range(n + m, m - n).is_finite_set is True
    assert Range(n, n + m + n).is_finite_set is True
    assert Range(n, oo).is_finite_set is False
    assert Range(-oo, n).is_finite_set is False
    assert Range(n, -oo).is_finite_set is True
    assert Range(oo, n).is_finite_set is True

