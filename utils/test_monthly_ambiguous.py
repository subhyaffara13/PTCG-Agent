
def test_monthly_ambiguous():
    rng = DatetimeIndex(["1/31/2000", "2/29/2000", "3/31/2000"])
    assert rng.inferred_freq == "ME"

