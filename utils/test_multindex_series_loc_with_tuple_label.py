
def test_multindex_series_loc_with_tuple_label():
    # GH#43908
    mi = MultiIndex.from_tuples([(1, 2), (3, (4, 5))])
    ser = Series([1, 2], index=mi)
    result = ser.loc[(3, (4, 5))]
    assert result == 2

