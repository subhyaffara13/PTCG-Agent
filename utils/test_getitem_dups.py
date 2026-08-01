
def test_getitem_dups():
    ser = Series(range(5), index=["A", "A", "B", "C", "C"], dtype=np.int64)
    expected = Series([3, 4], index=["C", "C"], dtype=np.int64)
    result = ser["C"]
    tm.assert_series_equal(result, expected)

