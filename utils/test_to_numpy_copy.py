
def test_to_numpy_copy(arr, as_series, using_infer_string):
    obj = pd.Index(arr, copy=False)
    if as_series:
        obj = Series(obj.values, copy=False)

    # no copy by default
    result = obj.to_numpy()
    if using_infer_string and arr.dtype == object and obj.dtype.storage == "pyarrow":
        assert np.shares_memory(arr, result) is False
    else:
        assert np.shares_memory(arr, result) is True

    result = obj.to_numpy(copy=False)
    if using_infer_string and arr.dtype == object and obj.dtype.storage == "pyarrow":
        assert np.shares_memory(arr, result) is False
    else:
        assert np.shares_memory(arr, result) is True

    # copy=True
    result = obj.to_numpy(copy=True)
    assert np.shares_memory(arr, result) is False


def test_to_numpy_copy():
    # to_numpy can be zero-copy if no missing values
    arr = pd.array([True, False, True], dtype="boolean")
    result = arr.to_numpy(dtype=bool)
    result[0] = False
    tm.assert_extension_array_equal(
        arr, pd.array([False, False, True], dtype="boolean")
    )

    arr = pd.array([True, False, True], dtype="boolean")
    result = arr.to_numpy(dtype=bool, copy=True)
    result[0] = False
    tm.assert_extension_array_equal(arr, pd.array([True, False, True], dtype="boolean"))


def test_to_numpy_copy():
    # to_numpy can be zero-copy if no missing values
    arr = pd.array([0.1, 0.2, 0.3], dtype="Float64")
    result = arr.to_numpy(dtype="float64")
    result[0] = 10
    tm.assert_extension_array_equal(arr, pd.array([10, 0.2, 0.3], dtype="Float64"))

    arr = pd.array([0.1, 0.2, 0.3], dtype="Float64")
    result = arr.to_numpy(dtype="float64", copy=True)
    result[0] = 10
    tm.assert_extension_array_equal(arr, pd.array([0.1, 0.2, 0.3], dtype="Float64"))

