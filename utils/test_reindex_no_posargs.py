
def test_reindex_no_posargs():
    # GH 40980
    ser = Series([1, 2])
    result = ser.reindex(index=[1, 0])
    expected = Series([2, 1], index=[1, 0])
    tm.assert_series_equal(result, expected)

