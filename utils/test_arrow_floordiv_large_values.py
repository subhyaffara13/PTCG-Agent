
def test_arrow_floordiv_large_values():
    # GH 56645
    a = pd.Series([1425801600000000000], dtype="int64[pyarrow]")
    expected = pd.Series([1425801600000], dtype="int64[pyarrow]")
    result = a // 1_000_000
    tm.assert_series_equal(result, expected)

