
def test_to_numpy_dtype(as_series):
    tz = "US/Eastern"
    obj = pd.DatetimeIndex(["2000", "2001"], tz=tz)
    if as_series:
        obj = Series(obj)

    # preserve tz by default
    result = obj.to_numpy()
    expected = np.array(
        [Timestamp("2000", tz=tz), Timestamp("2001", tz=tz)], dtype=object
    )
    tm.assert_numpy_array_equal(result, expected)

    result = obj.to_numpy(dtype="object")
    tm.assert_numpy_array_equal(result, expected)

    result = obj.to_numpy(dtype="M8[ns]")
    expected = np.array(["2000-01-01T05", "2001-01-01T05"], dtype="M8[ns]")
    tm.assert_numpy_array_equal(result, expected)


def test_to_numpy_dtype(box, dtype):
    con = pd.Series if box else pd.array
    arr = con([0.0, 1.0], dtype="Float64")

    result = arr.to_numpy(dtype=dtype)
    expected = np.array([0, 1], dtype=dtype)
    tm.assert_numpy_array_equal(result, expected)


def test_to_numpy_dtype(dtype, in_series):
    a = pd.array([0, 1], dtype="Int64")
    if in_series:
        a = pd.Series(a)

    result = a.to_numpy(dtype=dtype)
    expected = np.array([0, 1], dtype=dtype)
    tm.assert_numpy_array_equal(result, expected)

