
def test_partial_string_timestamp_multiindex_daily_resolution(df):
    # GH12685 (partial string with daily resolution or below)
    result = df.loc[IndexSlice["2013-03":"2013-03", :], :]
    expected = df.iloc[118:180]
    tm.assert_frame_equal(result, expected)

