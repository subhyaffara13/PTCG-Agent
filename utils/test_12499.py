
def test_12499():
    # TODO: OP in GH#12499 used np.datetim64("NaT") instead of pd.NaT,
    #  which has consequences for the expected df["two"] (though i think at
    #  the time it might not have because of a separate bug). See if it makes
    #  a difference which one we use here.
    ts = Timestamp("2016-03-01 03:13:22.98986", tz="UTC")

    data = [{"one": 0, "two": ts}]
    orig = DataFrame(data)
    df = orig.copy()
    df.loc[1] = [np.nan, NaT]

    expected = DataFrame(
        {"one": [0, np.nan], "two": Series([ts, NaT], dtype="datetime64[ns, UTC]")}
    )
    tm.assert_frame_equal(df, expected)

    data = [{"one": 0, "two": ts}]
    df = orig.copy()
    df.loc[1, :] = [np.nan, NaT]
    tm.assert_frame_equal(df, expected)

