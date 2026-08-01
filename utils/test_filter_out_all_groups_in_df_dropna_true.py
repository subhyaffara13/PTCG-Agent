
def test_filter_out_all_groups_in_df_dropna_true():
    # GH12768
    df = DataFrame({"a": [1, 1, 2], "b": [1, 2, 0]})
    res = df.groupby("a")
    res = res.filter(lambda x: x["b"].sum() > 5, dropna=True)
    expected = DataFrame({"a": [], "b": []}, dtype="int64")
    tm.assert_frame_equal(expected, res)

