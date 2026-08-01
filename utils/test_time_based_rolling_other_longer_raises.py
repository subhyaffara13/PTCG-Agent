
def test_time_based_rolling_other_longer_raises(func):
    # GH#62937
    idx_short = date_range("2020-01-01", periods=3, freq="D")
    idx_long = date_range("2020-01-01", periods=5, freq="D")
    s = Series([1, 2, 3], index=idx_short)
    other = Series([1, 2, 3, 4, 5], index=idx_long)
    msg = "Variable rolling window requires .* Got 3 < 5"
    with pytest.raises(ValueError, match=msg):
        getattr(s.rolling("2D"), func)(other)

