
def test_rolling_mean_sum_floating_artifacts():
    # GH 42064.

    sr = Series([1 / 3, 4, 0, 0, 0, 0, 0])
    r = sr.rolling(3)
    result = r.mean()
    assert (result[-3:] == 0).all()
    result = r.sum()
    assert (result[-3:] == 0).all()

