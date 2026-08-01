
def test_loc_boolean_indexer_non_matching_index():
    # GH#46551
    ser = Series([1])
    result = ser.loc[Series([NA, False], dtype="boolean")]
    expected = Series([], dtype="int64")
    tm.assert_series_equal(result, expected)

