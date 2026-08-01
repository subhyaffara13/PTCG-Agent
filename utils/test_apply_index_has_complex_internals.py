
def test_apply_index_has_complex_internals(index):
    # GH 31248
    df = DataFrame({"group": [1, 1, 2], "value": [0, 1, 0]}, index=index)
    result = df.groupby("group", group_keys=False).apply(lambda x: x)
    tm.assert_frame_equal(result, df[["value"]])

