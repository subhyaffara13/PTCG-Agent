
def test_pickle_datetimes(datetime_series, temp_file):
    unp_ts = tm.round_trip_pickle(datetime_series, temp_file)
    tm.assert_series_equal(unp_ts, datetime_series)

