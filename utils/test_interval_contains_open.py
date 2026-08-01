
def test_interval_contains_open():
    assert mtransforms._interval_contains_open((0, 1), 0.5)
    assert not mtransforms._interval_contains_open((0, 1), 0)
    assert not mtransforms._interval_contains_open((0, 1), 1)
    assert not mtransforms._interval_contains_open((0, 1), -1)
    assert not mtransforms._interval_contains_open((0, 1), 2)
    assert mtransforms._interval_contains_open((1, 0), 0.5)

