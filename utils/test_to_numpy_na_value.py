
def test_to_numpy_na_value(dtype):
    # GH#48951
    ser = Series([1, 2, NA, 4])
    result = ser.to_numpy(dtype=dtype, na_value=0)
    expected = np.array([1, 2, 0, 4], dtype=dtype)
    tm.assert_numpy_array_equal(result, expected)


def test_to_numpy_na_value(box):
    con = pd.Series if box else pd.array

    arr = con([0.0, 1.0, None], dtype="Float64")
    result = arr.to_numpy(dtype=object, na_value=None)
    expected = np.array([0.0, 1.0, None], dtype="object")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.to_numpy(dtype=bool, na_value=False)
    expected = np.array([False, True, False], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.to_numpy(dtype="int64", na_value=-99)
    expected = np.array([0, 1, -99], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)


def test_to_numpy_na_value(dtype, nulls_fixture):
    na_value = nulls_fixture
    arr = pd.array(["a", pd.NA, "b"], dtype=dtype)
    result = arr.to_numpy(na_value=na_value)
    expected = np.array(["a", na_value, "b"], dtype=object)
    tm.assert_numpy_array_equal(result, expected)

