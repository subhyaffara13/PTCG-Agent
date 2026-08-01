
def test_speed():
    # this should return in 0.0s. If it takes forever, it's wrong.
    assert x.diff(x, 10**8) == 0

