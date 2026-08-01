
def test_where_sparse():
    # GH#17198 make sure we dont get an AttributeError for sp_index
    ser = Series(pd.arrays.SparseArray([1, 2]))
    result = ser.where(ser >= 2, 0)
    expected = Series(pd.arrays.SparseArray([0, 2]))
    tm.assert_series_equal(result, expected)

