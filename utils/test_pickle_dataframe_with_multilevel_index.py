
def test_pickle_dataframe_with_multilevel_index(
    multiindex_year_month_day_dataframe_random_data,
    multiindex_dataframe_random_data,
    temp_file,
):
    ymd = multiindex_year_month_day_dataframe_random_data
    frame = multiindex_dataframe_random_data

    def _test_roundtrip(frame, temp_file):
        unpickled = tm.round_trip_pickle(frame, temp_file)
        tm.assert_frame_equal(frame, unpickled)

    _test_roundtrip(frame, temp_file)
    _test_roundtrip(frame.T, temp_file)
    _test_roundtrip(ymd, temp_file)
    _test_roundtrip(ymd.T, temp_file)

