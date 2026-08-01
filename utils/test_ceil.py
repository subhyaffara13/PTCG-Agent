
def test_ceil():
    a = ceil(interval(0.2, 0.5))
    assert a.start == 1
    assert a.end == 1

    a = ceil(interval(0.5, 1.5))
    assert a.start == 1
    assert a.end == 2
    assert a.is_valid is None

    a = ceil(interval(-5, 5))
    assert a.is_valid is None

    a = ceil(5.4)
    assert a.start == 6
    assert a.end == 6

