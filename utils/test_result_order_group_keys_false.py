
def test_result_order_group_keys_false():
    # GH 34998
    # apply result order should not depend on whether index is the same or just equal
    df = DataFrame({"A": [2, 1, 2], "B": [1, 2, 3]})
    result = df.groupby("A", group_keys=False).apply(lambda x: x)
    expected = df.groupby("A", group_keys=False).apply(lambda x: x.copy())
    tm.assert_frame_equal(result, expected)

