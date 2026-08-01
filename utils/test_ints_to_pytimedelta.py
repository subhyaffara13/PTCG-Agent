
def test_ints_to_pytimedelta(unit):
    # tests for non-nanosecond cases
    arr = np.arange(6, dtype=np.int64).view(f"m8[{unit}]")

    res = ints_to_pytimedelta(arr, box=False)
    # For non-nanosecond, .astype(object) gives pytimedelta objects
    #  instead of integers
    expected = arr.astype(object)
    tm.assert_numpy_array_equal(res, expected)

    res = ints_to_pytimedelta(arr, box=True)
    expected = np.array([Timedelta(x) for x in arr], dtype=object)
    tm.assert_numpy_array_equal(res, expected)

