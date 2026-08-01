
def test_nullable_integer_to_datetime():
    # Test for #30050
    ser = Series([1, 2, None, 2**61, None], dtype="Int64")
    ser_copy = ser.copy()

    res = to_datetime(ser, unit="ns")

    expected = Series(
        [
            np.datetime64("1970-01-01 00:00:00.000000001"),
            np.datetime64("1970-01-01 00:00:00.000000002"),
            np.datetime64("NaT", "ns"),
            np.datetime64("2043-01-25 23:56:49.213693952"),
            np.datetime64("NaT", "ns"),
        ]
    )
    tm.assert_series_equal(res, expected)
    # Check that ser isn't mutated
    tm.assert_series_equal(ser, ser_copy)

