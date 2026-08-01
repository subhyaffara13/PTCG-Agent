
def test_getitem_loc_commutability(multiindex_year_month_day_dataframe_random_data):
    df = multiindex_year_month_day_dataframe_random_data
    ser = df["A"]
    result = ser[2000, 5]
    expected = df.loc[2000, 5]["A"]
    tm.assert_series_equal(result, expected)

