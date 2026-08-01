
def test_transform_numeric_ret(cols, expected, agg_func):
    # GH#19200 and GH#27469
    df = DataFrame(
        {"a": date_range("2018-01-01", periods=3), "b": range(3), "c": range(7, 10)}
    )
    result = df.groupby("b")[cols].transform(agg_func)

    if agg_func == "rank":
        expected = expected.astype("float")
    elif agg_func == "size" and cols == ["a", "c"]:
        # transform("size") returns a Series
        expected = expected["a"].rename(None)
    tm.assert_equal(result, expected)

