
def test_datetime_subclass(klass):
    # GH 25851
    # ensure that subclassed datetime works with
    # array_to_datetime

    arr = np.array([klass(2000, 1, 1)], dtype=object)
    result, _ = tslib.array_to_datetime(arr)

    expected = np.array(["2000-01-01T00:00:00.000000"], dtype="M8[us]")
    tm.assert_numpy_array_equal(result, expected)

