
def test_not_monotonic():
    rng = DatetimeIndex(["1/31/2000", "1/31/2001", "1/31/2002"])
    rng = rng[::-1]

    assert rng.inferred_freq == "-1YE-JAN"

