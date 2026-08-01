
def test_nonagg_agg():
    # GH 35490 - Single/Multiple agg of non-agg function give same results
    # TODO: agg should raise for functions that don't aggregate
    df = DataFrame({"a": [1, 1, 2, 2], "b": [1, 2, 2, 1]})
    g = df.groupby("a")

    result = g.agg(["cumsum"])
    result.columns = result.columns.droplevel(-1)
    expected = g.agg("cumsum")

    tm.assert_frame_equal(result, expected)

