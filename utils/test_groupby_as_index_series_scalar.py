
def test_groupby_as_index_series_scalar(df):
    grouped = df.groupby(["A", "B"], as_index=False)

    # GH #421

    result = grouped["C"].agg(len)
    expected = grouped.agg(len).loc[:, ["A", "B", "C"]]
    tm.assert_frame_equal(result, expected)

