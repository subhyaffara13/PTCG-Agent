
def test_apply_index_date_object():
    # GH 5789
    # don't auto coerce dates
    ts = [
        "2011-05-16 00:00",
        "2011-05-16 01:00",
        "2011-05-16 02:00",
        "2011-05-16 03:00",
        "2011-05-17 02:00",
        "2011-05-17 03:00",
        "2011-05-17 04:00",
        "2011-05-17 05:00",
        "2011-05-18 02:00",
        "2011-05-18 03:00",
        "2011-05-18 04:00",
        "2011-05-18 05:00",
    ]
    df = DataFrame([row.split() for row in ts], columns=["date", "time"])
    df["value"] = [
        1.40893,
        1.40760,
        1.40750,
        1.40649,
        1.40893,
        1.40760,
        1.40750,
        1.40649,
        1.40893,
        1.40760,
        1.40750,
        1.40649,
    ]
    exp_idx = Index(["2011-05-16", "2011-05-17", "2011-05-18"], name="date")
    expected = Series(["00:00", "02:00", "02:00"], index=exp_idx)
    result = df.groupby("date").apply(lambda x: x["time"][x["value"].idxmax()])
    tm.assert_series_equal(result, expected)

