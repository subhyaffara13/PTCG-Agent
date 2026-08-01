
def test_series_getitem_indexing_errors(
    multiindex_year_month_day_dataframe_random_data,
    indexer,
    expected_error,
    expected_error_msg,
):
    s = multiindex_year_month_day_dataframe_random_data["A"]
    with pytest.raises(expected_error, match=expected_error_msg):
        indexer(s)

