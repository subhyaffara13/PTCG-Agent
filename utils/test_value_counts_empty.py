
def test_value_counts_empty():
    ser = pd.Series([], dtype="Float64")
    result = ser.value_counts()
    idx = pd.Index([], dtype="Float64")
    assert idx.dtype == "Float64"
    expected = pd.Series([], index=idx, dtype="Int64", name="count")
    tm.assert_series_equal(result, expected)


def test_value_counts_empty():
    # https://github.com/pandas-dev/pandas/issues/33317
    ser = pd.Series([], dtype="Int64")
    result = ser.value_counts()
    idx = pd.Index([], dtype=ser.dtype)
    assert idx.dtype == ser.dtype
    expected = pd.Series([], index=idx, dtype="Int64", name="count")
    tm.assert_series_equal(result, expected)

