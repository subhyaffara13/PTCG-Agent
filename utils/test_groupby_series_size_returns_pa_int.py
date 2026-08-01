
def test_groupby_series_size_returns_pa_int(data):
    # GH 54132
    ser = pd.Series(data[:3], index=["a", "a", "b"])
    result = ser.groupby(level=0).size()
    expected = pd.Series([2, 1], dtype="int64[pyarrow]", index=["a", "b"])
    tm.assert_series_equal(result, expected)

