
def test_resample_groupby_agg_listlike():
    # GH 42905
    ts = Timestamp("2021-02-28 00:00:00")
    df = DataFrame({"class": ["beta"], "value": [69]}, index=Index([ts], name="date"))
    resampled = df.groupby("class").resample("ME")["value"]
    result = resampled.agg(["sum", "size"])
    expected = DataFrame(
        [[69, 1]],
        index=pd.MultiIndex.from_tuples([("beta", ts)], names=["class", "date"]),
        columns=["sum", "size"],
    )
    tm.assert_frame_equal(result, expected)

