
def test_parsing_valid_dates(data, expected):
    arr = np.array(data, dtype=object)
    result, _ = tslib.array_to_datetime(arr)

    expected = np.array(expected, dtype="M8[us]")
    tm.assert_numpy_array_equal(result, expected)

