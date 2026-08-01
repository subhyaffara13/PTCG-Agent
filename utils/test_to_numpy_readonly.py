
def test_to_numpy_readonly():
    arr = pd.array([True, False, True], dtype="boolean")
    arr._readonly = True
    result = arr.to_numpy(dtype=bool)
    assert not result.flags.writeable

    result = arr.to_numpy(dtype="int64")
    assert result.flags.writeable


def test_to_numpy_readonly():
    arr = pd.array([0.1, 0.2, 0.3], dtype="Float64")
    arr._readonly = True
    result = arr.to_numpy(dtype="float64")
    assert not result.flags.writeable

    result = arr.to_numpy(dtype="float64", copy=True)
    assert result.flags.writeable

    result = arr.to_numpy(dtype="float32")
    assert result.flags.writeable

    result = arr.to_numpy(dtype="object")
    assert result.flags.writeable


def test_to_numpy_readonly():
    arr = pd.array([0, 1], dtype="Int64")
    arr._readonly = True
    result = arr.to_numpy()
    assert not result.flags.writeable

    result = arr.to_numpy(dtype="int64", copy=True)
    assert result.flags.writeable

    result = arr.to_numpy(dtype="int32")
    assert result.flags.writeable

    result = arr.to_numpy(dtype="object")
    assert result.flags.writeable


def test_to_numpy_readonly():
    arr = NumpyExtensionArray(np.array([1, 2, 3]))
    arr._readonly = True
    result = arr.to_numpy()
    assert not result.flags.writeable

    result = arr.to_numpy(copy=True)
    assert result.flags.writeable

    result = arr.to_numpy(dtype="f8")
    assert result.flags.writeable


def test_to_numpy_readonly(dtype):
    arr = pd.array(["a", pd.NA, "b"], dtype=dtype)
    arr._readonly = True
    result = arr.to_numpy()
    if dtype.storage == "python":
        assert not result.flags.writeable
    else:
        assert result.flags.writeable

