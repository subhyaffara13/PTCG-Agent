
def test_groupby_selection_other_methods(df):
    # some methods which require DatetimeIndex
    rng = date_range("2014", periods=len(df))
    df.columns.name = "foo"
    df.index = rng

    g = df.groupby(["A"])[["C"]]
    g_exp = df[["C"]].groupby(df["A"])

    # methods which aren't just .foo()
    tm.assert_frame_equal(g.apply(lambda x: x.sum()), g_exp.apply(lambda x: x.sum()))

    tm.assert_frame_equal(g.resample("D").mean(), g_exp.resample("D").mean())
    tm.assert_frame_equal(g.resample("D").ohlc(), g_exp.resample("D").ohlc())

    tm.assert_frame_equal(
        g.filter(lambda x: len(x) == 3), g_exp.filter(lambda x: len(x) == 3)
    )

