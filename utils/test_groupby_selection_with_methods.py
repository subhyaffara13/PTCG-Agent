
def test_groupby_selection_with_methods(df, method):
    # some methods which require DatetimeIndex
    rng = date_range("2014", periods=len(df))
    df.index = rng

    g = df.groupby(["A"])[["C"]]
    g_exp = df[["C"]].groupby(df["A"])
    # TODO check groupby with > 1 col ?

    res = getattr(g, method)()
    exp = getattr(g_exp, method)()

    # should always be frames!
    tm.assert_frame_equal(res, exp)

