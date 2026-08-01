
def test_reset_index_rename_multiindex(float_frame):
    # GH 6878
    stacked_df = float_frame.stack()[::2]
    stacked_df = DataFrame({"foo": stacked_df, "bar": stacked_df})

    names = ["first", "second"]
    stacked_df.index.names = names

    result = stacked_df.reset_index()
    expected = stacked_df.reset_index(names=["new_first", "new_second"])
    tm.assert_series_equal(result["first"], expected["new_first"], check_names=False)
    tm.assert_series_equal(result["second"], expected["new_second"], check_names=False)

