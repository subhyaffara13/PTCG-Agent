
def test_apply_nonmonotonic_float_index(arg, idx):
    # GH 34455
    df = DataFrame({"grp": arg, "col": arg}, index=idx)
    result = df.groupby("grp", group_keys=False).apply(lambda x: x)
    expected = df[["col"]]
    tm.assert_frame_equal(result, expected)

