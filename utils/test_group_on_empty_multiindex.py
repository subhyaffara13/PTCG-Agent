
def test_group_on_empty_multiindex(transformation_func, request):
    # GH 47787
    # With one row, those are transforms so the schema should be the same
    df = DataFrame(
        data=[[1, Timestamp("today"), 3, 4]],
        columns=["col_1", "col_2", "col_3", "col_4"],
    )
    df["col_3"] = df["col_3"].astype(int)
    df["col_4"] = df["col_4"].astype(int)
    df = df.set_index(["col_1", "col_2"])
    result = df.iloc[:0].groupby(["col_1"]).transform(transformation_func)
    expected = df.groupby(["col_1"]).transform(transformation_func).iloc[:0]
    if transformation_func in ("diff", "shift"):
        expected = expected.astype(int)
    tm.assert_equal(result, expected)

    result = df["col_3"].iloc[:0].groupby(["col_1"]).transform(transformation_func)
    expected = df["col_3"].groupby(["col_1"]).transform(transformation_func).iloc[:0]
    if transformation_func in ("diff", "shift"):
        expected = expected.astype(int)
    tm.assert_equal(result, expected)

