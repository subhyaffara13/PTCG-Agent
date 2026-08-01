
def test_frame_getitem_toplevel(
    multiindex_dataframe_random_data, indexer, expected_slice
):
    df = multiindex_dataframe_random_data.T
    expected = df.reindex(columns=df.columns[expected_slice])
    expected.columns = expected.columns.droplevel(0)
    result = indexer(df)
    tm.assert_frame_equal(result, expected)

