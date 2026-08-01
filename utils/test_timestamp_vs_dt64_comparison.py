
def test_timestamp_vs_dt64_comparison():
    # GH#60937
    left = pd.Series(["2016-01-01"], dtype="timestamp[ns][pyarrow]")
    right = left.astype("datetime64[ns]")

    result = left == right
    expected = pd.Series([True], dtype="bool[pyarrow]")
    tm.assert_series_equal(result, expected)

    result = right == left
    tm.assert_series_equal(result, expected)

