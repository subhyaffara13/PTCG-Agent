
def test_grouping_ndarray(df):
    grouped = df.groupby(df["A"].values)
    grouped2 = df.groupby(df["A"].rename(None))

    result = grouped.sum()
    expected = grouped2.sum()
    tm.assert_frame_equal(result, expected)

