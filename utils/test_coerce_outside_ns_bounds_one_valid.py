
def test_coerce_outside_ns_bounds_one_valid():
    arr = np.array(["1/1/1000", "1/1/2000"], dtype=object)
    result, _ = tslib.array_to_datetime(arr, errors="coerce")

    expected = ["1000-01-01T00:00:00.000000000", "2000-01-01T00:00:00.000000000"]
    expected = np.array(expected, dtype="M8[us]")

    tm.assert_numpy_array_equal(result, expected)

