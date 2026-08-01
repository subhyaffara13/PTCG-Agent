
def test_apply_str_with_args(df, args, kwargs):
    # GH#46479
    gb = df.groupby("A")
    result = gb.apply("sum", *args, **kwargs)
    expected = gb.sum(numeric_only=True)
    tm.assert_frame_equal(result, expected)

