
def test_arrow_timestamp_resample_keep_index_name():
    # https://github.com/pandas-dev/pandas/issues/61222
    idx = Series(date_range("2020-01-01", periods=5), dtype="timestamp[ns][pyarrow]")
    expected = Series(np.arange(5, dtype=np.float64), index=idx)
    expected.index.name = "index_name"
    result = expected.resample("1D").mean()
    tm.assert_series_equal(result, expected)

