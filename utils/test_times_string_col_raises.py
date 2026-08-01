
def test_times_string_col_raises():
    # GH 43265
    df = DataFrame(
        {"A": np.arange(10.0), "time_col": date_range("2000", freq="D", periods=10)}
    )
    with pytest.raises(ValueError, match="times must be datetime64"):
        df.ewm(halflife="1 day", min_periods=0, times="time_col")

