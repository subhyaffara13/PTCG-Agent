
def test_is_monotonic_with_nans(values, attr):
    # GH: 37220
    idx = MultiIndex.from_tuples(values, names=["test"])
    assert getattr(idx, attr) is False

