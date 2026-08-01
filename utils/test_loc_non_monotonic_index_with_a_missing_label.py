
def test_loc_non_monotonic_index_with_a_missing_label():
    msg = "Cannot get left slice bound for non-monotonic index with a missing label 4"
    ser = Series([3, 6, 7, 6], index=[3, 8, 7, 6])
    with pytest.raises(KeyError, match=msg):
        ser.loc[4:7]

