
def test_merge_cross_series():
    # GH#54055
    ls = Series([1, 2, 3, 4], index=[1, 2, 3, 4], name="left")
    rs = Series([3, 4, 5, 6], index=[3, 4, 5, 6], name="right")
    res = merge(ls, rs, how="cross")

    expected = merge(ls.to_frame(), rs.to_frame(), how="cross")
    tm.assert_frame_equal(res, expected)

