
def test_parsing_non_iso_timezone_offset():
    dt_string = "01-01-2013T00:00:00.000000000+0000"
    arr = np.array([dt_string], dtype=object)

    with tm.assert_produces_warning(None):
        # GH#50949 should not get tzlocal-deprecation warning here
        result, result_tz = tslib.array_to_datetime(arr)
    expected = np.array([np.datetime64("2013-01-01 00:00:00.000000000")])

    tm.assert_numpy_array_equal(result, expected)
    assert result_tz is timezone.utc

