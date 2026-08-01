
def test_filter_has_access_to_grouped_cols():
    df = DataFrame([[1, 2], [1, 3], [5, 6]], columns=["A", "B"])
    g = df.groupby("A")
    # previously didn't have access to col A #????
    filt = g.filter(lambda x: x["A"].sum() == 2)
    tm.assert_frame_equal(filt, df.iloc[[0, 1]])

