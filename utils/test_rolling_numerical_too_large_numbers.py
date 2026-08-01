
def test_rolling_numerical_too_large_numbers():
    # GH: 11645
    dates = date_range("2015-01-01", periods=10, freq="D")
    ds = Series(data=range(10), index=dates, dtype=np.float64)
    ds.iloc[2] = -9e33
    result = ds.rolling(5).mean()
    expected = Series(
        [
            np.nan,
            np.nan,
            np.nan,
            np.nan,
            -1.8e33,
            -1.8e33,
            -1.8e33,
            5.0,
            6.0,
            7.0,
        ],
        index=dates,
    )
    tm.assert_series_equal(result, expected)

