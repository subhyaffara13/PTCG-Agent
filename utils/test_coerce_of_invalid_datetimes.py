
def test_coerce_of_invalid_datetimes():
    arr = np.array(["01-01-2013", "not_a_date", "1"], dtype=object)
    # With coercing, the invalid dates becomes iNaT
    result, _ = tslib.array_to_datetime(arr, errors="coerce")
    expected = ["2013-01-01T00:00:00.000000000", iNaT, iNaT]
    tm.assert_numpy_array_equal(result, np.array(expected, dtype="M8[us]"))

    # With coercing, the invalid dates becomes iNaT
    result, _ = tslib.array_to_datetime(arr, errors="coerce")
    expected = ["2013-01-01T00:00:00.000000000", iNaT, iNaT]

    tm.assert_numpy_array_equal(result, np.array(expected, dtype="M8[us]"))

