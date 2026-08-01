
def test_astype():
    arr = DummyArray(np.array([1, 2, 3]))
    expected = np.array([1, 2, 3], dtype=object)

    result = arr.astype(object)
    tm.assert_numpy_array_equal(result, expected)

    result = arr.astype("object")
    tm.assert_numpy_array_equal(result, expected)


def test_astype(idx):
    expected = idx.copy()
    actual = idx.astype("O")
    tm.assert_copy(actual.levels, expected.levels)
    tm.assert_copy(actual.codes, expected.codes)
    assert actual.names == list(expected.names)

    with pytest.raises(TypeError, match="^Setting.*dtype.*object"):
        idx.astype(np.dtype(int))


def test_astype(using_infer_string):
    # with missing values
    arr = pd.array([True, False, None], dtype="boolean")

    with pytest.raises(ValueError, match="cannot convert NA to integer"):
        arr.astype("int64")

    with pytest.raises(ValueError, match="cannot convert float NaN to"):
        arr.astype("bool")

    result = arr.astype("float64")
    expected = np.array([1, 0, np.nan], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.astype("str")
    if using_infer_string:
        expected = pd.array(
            ["True", "False", None], dtype=pd.StringDtype(na_value=np.nan)
        )
        tm.assert_extension_array_equal(result, expected)
    else:
        expected = np.array(["True", "False", "<NA>"], dtype=f"{tm.ENDIAN}U5")
        tm.assert_numpy_array_equal(result, expected)

    # no missing values
    arr = pd.array([True, False, True], dtype="boolean")
    result = arr.astype("int64")
    expected = np.array([1, 0, 1], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.astype("bool")
    expected = np.array([True, False, True], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)


def test_astype():
    # with missing values
    arr = pd.array([0.1, 0.2, None], dtype="Float64")

    with pytest.raises(ValueError, match="cannot convert NA to integer"):
        arr.astype("int64")

    with pytest.raises(ValueError, match="cannot convert float NaN to bool"):
        arr.astype("bool")

    result = arr.astype("float64")
    expected = np.array([0.1, 0.2, np.nan], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

    # no missing values
    arr = pd.array([0.0, 1.0, 0.5], dtype="Float64")
    result = arr.astype("int64")
    expected = np.array([0, 1, 0], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.astype("bool")
    expected = np.array([False, True, True], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)


def test_astype(all_data):
    all_data = all_data[:10]

    ints = all_data[~all_data.isna()]
    mixed = all_data
    dtype = Int8Dtype()

    # coerce to same type - ints
    s = pd.Series(ints)
    result = s.astype(all_data.dtype)
    expected = pd.Series(ints)
    tm.assert_series_equal(result, expected)

    # coerce to same other - ints
    s = pd.Series(ints)
    result = s.astype(dtype)
    expected = pd.Series(ints, dtype=dtype)
    tm.assert_series_equal(result, expected)

    # coerce to same numpy_dtype - ints
    s = pd.Series(ints)
    result = s.astype(all_data.dtype.numpy_dtype)
    expected = pd.Series(ints._data.astype(all_data.dtype.numpy_dtype))
    tm.assert_series_equal(result, expected)

    # coerce to same type - mixed
    s = pd.Series(mixed)
    result = s.astype(all_data.dtype)
    expected = pd.Series(mixed)
    tm.assert_series_equal(result, expected)

    # coerce to same other - mixed
    s = pd.Series(mixed)
    result = s.astype(dtype)
    expected = pd.Series(mixed, dtype=dtype)
    tm.assert_series_equal(result, expected)

    # coerce to same numpy_dtype - mixed
    s = pd.Series(mixed)
    msg = "cannot convert NA to integer"
    with pytest.raises(ValueError, match=msg):
        s.astype(all_data.dtype.numpy_dtype)

    # coerce to object
    s = pd.Series(mixed)
    result = s.astype("object")
    expected = pd.Series(np.asarray(mixed, dtype=object))
    tm.assert_series_equal(result, expected)

