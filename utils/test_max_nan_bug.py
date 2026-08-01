
def test_max_nan_bug():
    df = DataFrame(
        {
            "Unnamed: 0": ["-04-23", "-05-06", "-05-07"],
            "Date": [
                "2013-04-23 00:00:00",
                "2013-05-06 00:00:00",
                "2013-05-07 00:00:00",
            ],
            "app": Series([np.nan, np.nan, "OE"]),
            "File": ["log080001.log", "log.log", "xlsx"],
        }
    )
    gb = df.groupby("Date")
    r = gb[["File"]].max()
    e = gb["File"].max().to_frame()
    tm.assert_frame_equal(r, e)
    assert not r["File"].isna().any()

