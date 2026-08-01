
def test_preserve_on_ordered_ops(func, values):
    # gh-18502
    # preserve the categoricals on ops
    c = Categorical(["first", "second", "third", "fourth"], ordered=True)
    df = DataFrame({"payload": [-1, -2, -1, -2], "col": c})
    g = df.groupby("payload")
    result = getattr(g, func)()
    expected = DataFrame(
        {"payload": [-2, -1], "col": Series(values, dtype=c.dtype)}
    ).set_index("payload")
    tm.assert_frame_equal(result, expected)

    # we should also preserve categorical for SeriesGroupBy
    sgb = df.groupby("payload")["col"]
    result = getattr(sgb, func)()
    expected = expected["col"]
    tm.assert_series_equal(result, expected)

