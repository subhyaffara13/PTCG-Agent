
def test_filter_out_all_groups_in_df():
    # GH12768
    df = DataFrame({"a": [1, 1, 2], "b": [1, 2, 0]})
    res = df.groupby("a")
    res = res.filter(lambda x: x["b"].sum() > 5, dropna=False)
    expected = DataFrame({"a": [np.nan] * 3, "b": [np.nan] * 3})
    tm.assert_frame_equal(expected, res)

