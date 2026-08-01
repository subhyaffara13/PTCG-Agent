
def test_tz_localize_to_utc_copies():
    # GH#46460
    arr = np.arange(5, dtype="i8")
    result = tz_convert_from_utc(arr, tz=timezone.utc)
    tm.assert_numpy_array_equal(result, arr)
    assert not np.shares_memory(arr, result)

    result = tz_convert_from_utc(arr, tz=None)
    tm.assert_numpy_array_equal(result, arr)
    assert not np.shares_memory(arr, result)

