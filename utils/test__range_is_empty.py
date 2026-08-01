
def test_Range_is_empty():
    i = Symbol('i', integer=True)
    n = Symbol('n', negative=True, integer=True)
    p = Symbol('p', positive=True, integer=True)

    assert Range(0).is_empty
    assert not Range(1).is_empty
    assert Range(1, 0).is_empty
    assert not Range(-1, 0).is_empty
    assert Range(i).is_empty is None
    assert Range(n).is_empty
    assert Range(p).is_empty is False
    assert Range(n, 0).is_empty is False
    assert Range(n, p).is_empty is False
    assert Range(p, n).is_empty
    assert Range(n, -1).is_empty is None
    assert Range(p, n, -1).is_empty is False

