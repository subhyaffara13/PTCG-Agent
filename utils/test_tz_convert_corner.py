
def test_tz_convert_corner(arr):
    arr = np.array([iNaT], dtype=np.int64)
    result = tz_convert_from_utc(arr, timezones.maybe_get_tz("Asia/Tokyo"))
    tm.assert_numpy_array_equal(result, arr)

