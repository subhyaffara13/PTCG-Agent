
def test_interval_contains():
    assert mtransforms._interval_contains((0, 1), 0.5)
    assert mtransforms._interval_contains((0, 1), 0)
    assert mtransforms._interval_contains((0, 1), 1)
    assert not mtransforms._interval_contains((0, 1), -1)
    assert not mtransforms._interval_contains((0, 1), 2)
    assert mtransforms._interval_contains((1, 0), 0.5)

