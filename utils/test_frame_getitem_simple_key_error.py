
def test_frame_getitem_simple_key_error(
    multiindex_dataframe_random_data, indexer, expected_error_msg
):
    df = multiindex_dataframe_random_data.T
    with pytest.raises(KeyError, match=expected_error_msg):
        indexer(df)

