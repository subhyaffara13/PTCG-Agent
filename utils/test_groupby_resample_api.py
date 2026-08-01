
def test_groupby_resample_api():
    # GH 12448
    # .groupby(...).resample(...) hitting warnings
    # when appropriate
    df = DataFrame(
        {
            "date": date_range(start="2016-01-01", periods=4, freq="W"),
            "group": [1, 1, 2, 2],
            "val": [5, 6, 7, 8],
        }
    ).set_index("date")

    # replication step
    i = (
        date_range("2016-01-03", periods=8).tolist()
        + date_range("2016-01-17", periods=8).tolist()
    )
    index = pd.MultiIndex.from_arrays([[1] * 8 + [2] * 8, i], names=["group", "date"])
    expected = DataFrame({"val": [5] * 7 + [6] + [7] * 7 + [8]}, index=index)
    result = df.groupby("group").apply(lambda x: x.resample("1D").ffill())[["val"]]
    tm.assert_frame_equal(result, expected)

