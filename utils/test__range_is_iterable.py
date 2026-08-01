
def test_Range_is_iterable():
    assert Range(-100, 100).is_iterable is True
    assert Range(2, oo).is_iterable is False
    assert Range(-oo, 50).is_iterable is False
    assert Range(-oo, oo).is_iterable is False
    assert Range(oo, -oo).is_iterable is True
    assert Range(0, 0).is_iterable is True
    assert Range(oo, oo).is_iterable is True
    assert Range(-oo, -oo).is_iterable is True
    n = Symbol('n', integer=True)
    m = Symbol('m', integer=True)
    p = Symbol('p', integer=True, positive=True)
    assert Range(n, n + 49).is_iterable is True
    assert Range(n, 0).is_iterable is False
    assert Range(-3, n + 7).is_iterable is False
    assert Range(-3, p + 7).is_iterable is False # Should work with better __iter__
    assert Range(n, m).is_iterable is False
    assert Range(n + m, m - n).is_iterable is False
    assert Range(n, n + m + n).is_iterable is False
    assert Range(n, oo).is_iterable is False
    assert Range(-oo, n).is_iterable is False
    x = Symbol('x')
    assert Range(x, x + 49).is_iterable is False
    assert Range(x, 0).is_iterable is False
    assert Range(-3, x + 7).is_iterable is False
    assert Range(x, m).is_iterable is False
    assert Range(x + m, m - x).is_iterable is False
    assert Range(x, x + m + x).is_iterable is False
    assert Range(x, oo).is_iterable is False
    assert Range(-oo, x).is_iterable is False

