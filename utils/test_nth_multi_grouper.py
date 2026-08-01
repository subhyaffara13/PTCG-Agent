
def test_nth_multi_grouper(three_group):
    # PR 9090, related to issue 8979
    # test nth on multiple groupers
    grouped = three_group.groupby(["A", "B"])
    result = grouped.nth(0)
    expected = three_group.iloc[[0, 3, 4, 7]]
    tm.assert_frame_equal(result, expected)

