
def test_pickle_strings(string_series, temp_file):
    unp_series = tm.round_trip_pickle(string_series, temp_file)
    tm.assert_series_equal(unp_series, string_series)

