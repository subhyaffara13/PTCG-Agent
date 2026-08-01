
def test_tz_convert_readonly():
    # GH#35530
    arr = np.array([0], dtype=np.int64)
    arr.setflags(write=False)
    result = tz_convert_from_utc(arr, timezone.utc)
    tm.assert_numpy_array_equal(result, arr)

