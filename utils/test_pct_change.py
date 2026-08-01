
def test_pct_change(frame_or_series, freq, periods):
    # GH 21200, 21621, 30463
    vals = [3, np.nan, np.nan, np.nan, 1, 2, 4, 10, np.nan, 4]
    keys = ["a", "b"]
    key_v = np.repeat(keys, len(vals))
    df = DataFrame({"key": key_v, "vals": vals * 2})

    df_g = df
    grp = df_g.groupby(df.key)

    expected = grp["vals"].obj / grp["vals"].shift(periods) - 1

    gb = df.groupby("key")

    if frame_or_series is Series:
        gb = gb["vals"]
    else:
        expected = expected.to_frame("vals")

    result = gb.pct_change(periods=periods, freq=freq)
    tm.assert_equal(result, expected)

