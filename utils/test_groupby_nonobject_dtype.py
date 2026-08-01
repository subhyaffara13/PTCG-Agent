
def test_groupby_nonobject_dtype(multiindex_dataframe_random_data):
    key = multiindex_dataframe_random_data.index.codes[0]
    grouped = multiindex_dataframe_random_data.groupby(key)
    result = grouped.sum()

    expected = multiindex_dataframe_random_data.groupby(key.astype("O")).sum()
    assert result.index.dtype == np.int8
    assert expected.index.dtype == np.int64
    tm.assert_frame_equal(result, expected, check_index_type=False)

