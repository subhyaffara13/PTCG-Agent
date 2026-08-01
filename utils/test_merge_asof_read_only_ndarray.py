
def test_merge_asof_read_only_ndarray():
    # GH 53513
    left = pd.Series([2], index=[2], name="left")
    right = pd.Series([1], index=[1], name="right")
    # set to read-only
    left.index.values.flags.writeable = False
    right.index.values.flags.writeable = False
    result = merge_asof(left, right, left_index=True, right_index=True)
    expected = pd.DataFrame({"left": [2], "right": [1]}, index=[2])
    tm.assert_frame_equal(result, expected)

