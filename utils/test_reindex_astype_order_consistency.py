
def test_reindex_astype_order_consistency():
    # GH#17444
    ser = Series([1, 2, 3], index=[2, 0, 1])
    new_index = [0, 1, 2]
    temp_dtype = "category"
    new_dtype = str
    result = ser.reindex(new_index).astype(temp_dtype).astype(new_dtype)
    expected = ser.astype(temp_dtype).reindex(new_index).astype(new_dtype)
    tm.assert_series_equal(result, expected)

