
def test_filter_pdna_is_false():
    # in particular, dont raise in filter trying to call bool(pd.NA)
    df = DataFrame({"A": np.arange(8), "B": list("aabbbbcc"), "C": np.arange(8)})
    ser = df["B"]
    g_df = df.groupby(df["B"])
    g_s = ser.groupby(ser)

    func = lambda x: pd.NA
    res = g_df.filter(func)
    tm.assert_frame_equal(res, df.loc[[]])
    res = g_s.filter(func)
    tm.assert_series_equal(res, ser[[]])

