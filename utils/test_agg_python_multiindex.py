
def test_agg_python_multiindex(multiindex_dataframe_random_data):
    grouped = multiindex_dataframe_random_data.groupby(["A", "B"])

    result = grouped.agg("mean")
    expected = grouped.mean()
    tm.assert_frame_equal(result, expected)

