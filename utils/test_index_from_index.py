
def test_index_from_index():
    ser = Series([1, 2])
    idx = Index(ser)
    idx = Index(idx)
    expected = idx.copy(deep=True)
    ser.iloc[0] = 100
    tm.assert_index_equal(idx, expected)

