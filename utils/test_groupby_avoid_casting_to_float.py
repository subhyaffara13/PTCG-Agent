
def test_groupby_avoid_casting_to_float(func):
    # GH#37493
    val = 922337203685477580
    df = DataFrame({"a": 1, "b": [val]})
    result = getattr(df.groupby("a"), func)() - val
    expected = DataFrame({"b": [0]}, index=Index([1], name="a"))
    if func in ["cumsum", "cumprod"]:
        expected = expected.reset_index(drop=True)
    tm.assert_frame_equal(result, expected)

