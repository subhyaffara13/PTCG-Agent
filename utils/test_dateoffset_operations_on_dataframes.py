
def test_dateoffset_operations_on_dataframes(performance_warning):
    # GH 47953
    df = DataFrame({"T": [Timestamp("2019-04-30")], "D": [DateOffset(months=1)]})
    frameresult1 = df["T"] + 26 * df["D"]
    df2 = DataFrame(
        {
            "T": [Timestamp("2019-04-30"), Timestamp("2019-04-30")],
            "D": [DateOffset(months=1), DateOffset(months=1)],
        }
    )
    expecteddate = Timestamp("2021-06-30")
    with tm.assert_produces_warning(performance_warning):
        frameresult2 = df2["T"] + 26 * df2["D"]

    assert frameresult1[0] == expecteddate
    assert frameresult2[0] == expecteddate

