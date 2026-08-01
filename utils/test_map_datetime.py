
def test_map_datetime(datetime_series):
    # function
    result = datetime_series.map(lambda x: x * 2)
    tm.assert_series_equal(result, datetime_series * 2)

