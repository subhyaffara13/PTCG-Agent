
def test_parsing_timezone_offsets(dt_string, expected_tz):
    # All of these datetime strings with offsets are equivalent
    # to the same datetime after the timezone offset is added.
    arr = np.array(["01-01-2013 00:00:00"], dtype=object)
    expected, _ = tslib.array_to_datetime(arr)
    if "000000000" in dt_string:
        expected = expected.astype("M8[ns]")

    arr = np.array([dt_string], dtype=object)
    result, result_tz = tslib.array_to_datetime(arr)

    tm.assert_numpy_array_equal(result, expected)
    assert result_tz == timezone(timedelta(minutes=expected_tz))

