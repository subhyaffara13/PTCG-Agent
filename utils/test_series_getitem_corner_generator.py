
def test_series_getitem_corner_generator(
    multiindex_year_month_day_dataframe_random_data,
):
    s = multiindex_year_month_day_dataframe_random_data["A"]
    result = s[(x > 0 for x in s)]
    expected = s[s > 0]
    tm.assert_series_equal(result, expected)

