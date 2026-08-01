
def test_arrow_datetime_axis():
    # GH 55849
    expected = Series(
        np.arange(5, dtype=np.float64),
        index=Index(
            date_range("2020-01-01", periods=5), dtype="timestamp[ns][pyarrow]"
        ),
    )
    result = expected.rolling("1D").sum()
    tm.assert_series_equal(result, expected)

