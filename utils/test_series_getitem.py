
def test_series_getitem(multiindex_year_month_day_dataframe_random_data, indexer_sl):
    s = multiindex_year_month_day_dataframe_random_data["A"]
    expected = s.reindex(s.index[42:65])
    expected.index = expected.index.droplevel(0).droplevel(0)

    result = indexer_sl(s)[2000, 3]
    tm.assert_series_equal(result, expected)

