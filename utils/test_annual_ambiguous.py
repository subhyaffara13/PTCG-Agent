
def test_annual_ambiguous():
    rng = DatetimeIndex(["1/31/2000", "1/31/2001", "1/31/2002"])
    assert rng.inferred_freq == "YE-JAN"

