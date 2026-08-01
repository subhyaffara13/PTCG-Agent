
def test_frame_getitem_slice(multiindex_dataframe_random_data):
    df = multiindex_dataframe_random_data
    result = df.iloc[:4]
    expected = df[:4]
    tm.assert_frame_equal(result, expected)

