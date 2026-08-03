import sys

def test_to_numpy():
    if not np:
        skip("numpy not installed.")

    result = np.array([[1, 2], [3, 4]], dtype='complex')
    assert (to_numpy(m) == result).all()


def test_to_numpy():
    if sys.byteorder == 'little':
        assert_(sibc.to_numpy_code('native') == '<')
        assert_(sibc.to_numpy_code('swapped') == '>')
    else:
        assert_(sibc.to_numpy_code('native') == '>')
        assert_(sibc.to_numpy_code('swapped') == '<')
    assert_(sibc.to_numpy_code('native') == sibc.to_numpy_code('='))
    assert_(sibc.to_numpy_code('big') == '>')
    for code in ('little', '<', 'l', 'L', 'le'):
        assert_(sibc.to_numpy_code(code) == '<')
    for code in ('big', '>', 'b', 'B', 'be'):
        assert_(sibc.to_numpy_code(code) == '>')
    assert_raises(ValueError, sibc.to_numpy_code, 'silly string')


def test_to_numpy(arr, expected, zero_copy, index_or_series_or_array, using_nan_is_na):
    if not using_nan_is_na and arr[-1] is pd.NA:
        expected = np.array([0, pd.NA], dtype=object)

    box = index_or_series_or_array

    with tm.assert_produces_warning(None):
        thing = box(arr)

    result = thing.to_numpy()
    tm.assert_numpy_array_equal(result, expected)

    result = np.asarray(thing)
    tm.assert_numpy_array_equal(result, expected)

    # Additionally, we check the `copy=` semantics for array/asarray
    # (these are implemented by us via `__array__`).
    result_cp1 = np.array(thing, copy=True)
    result_cp2 = np.array(thing, copy=True)
    # When called with `copy=True` NumPy/we should ensure a copy was made
    assert not np.may_share_memory(result_cp1, result_cp2)

    if not np_version_gt2:
        # copy=False semantics are only supported in NumPy>=2.
        return

    if not zero_copy:
        with pytest.raises(ValueError, match="Unable to avoid copy while creating"):
            # An error is always acceptable for `copy=False`
            np.array(thing, copy=False)

    else:
        result_nocopy1 = np.array(thing, copy=False)
        result_nocopy2 = np.array(thing, copy=False)
        # If copy=False was given, these must share the same data
        assert np.may_share_memory(result_nocopy1, result_nocopy2)


def test_to_numpy(idx):
    result = idx.to_numpy()
    exp = idx.values
    tm.assert_numpy_array_equal(result, exp)


def test_to_numpy(box):
    con = pd.Series if box else pd.array
    # default (with or without missing values) -> object dtype
    arr = con([True, False, True], dtype="boolean")
    result = arr.to_numpy()
    expected = np.array([True, False, True], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)

    arr = con([True, False, None], dtype="boolean")
    result = arr.to_numpy()
    expected = np.array([True, False, pd.NA], dtype="object")
    tm.assert_numpy_array_equal(result, expected)

    arr = con([True, False, None], dtype="boolean")
    result = arr.to_numpy(dtype="str")
    expected = np.array([True, False, pd.NA], dtype=f"{tm.ENDIAN}U5")
    tm.assert_numpy_array_equal(result, expected)

    # no missing values -> can convert to bool, otherwise raises
    arr = con([True, False, True], dtype="boolean")
    result = arr.to_numpy(dtype="bool")
    expected = np.array([True, False, True], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)

    arr = con([True, False, None], dtype="boolean")
    with pytest.raises(ValueError, match="cannot convert to 'bool'-dtype"):
        result = arr.to_numpy(dtype="bool")

    # specify dtype and na_value
    arr = con([True, False, None], dtype="boolean")
    result = arr.to_numpy(dtype=object, na_value=None)
    expected = np.array([True, False, None], dtype="object")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.to_numpy(dtype=bool, na_value=False)
    expected = np.array([True, False, False], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.to_numpy(dtype="int64", na_value=-99)
    expected = np.array([1, 0, -99], dtype="int64")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.to_numpy(dtype="float64", na_value=np.nan)
    expected = np.array([1, 0, np.nan], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

    # converting to int or float without specifying na_value raises
    with pytest.raises(ValueError, match="cannot convert to 'int64'-dtype"):
        arr.to_numpy(dtype="int64")


def test_to_numpy(box, using_nan_is_na):
    con = pd.Series if box else pd.array

    # default (with or without missing values) -> object dtype
    arr = con([0.1, 0.2, 0.3], dtype="Float64")
    result = arr.to_numpy()
    expected = np.array([0.1, 0.2, 0.3], dtype="float64")
    # TODO: should this be object with `not using_nan_is_na` to avoid
    #  values-dependent behavior?
    tm.assert_numpy_array_equal(result, expected)

    arr = con([0.1, 0.2, None], dtype="Float64")
    result = arr.to_numpy()
    if using_nan_is_na:
        expected = np.array([0.1, 0.2, np.nan], dtype="float64")
    else:
        expected = np.array([0.1, 0.2, pd.NA], dtype=object)
    tm.assert_numpy_array_equal(result, expected)


def test_to_numpy():
    # GH#56991

    class MyStringArray(BaseMaskedArray):
        dtype = pd.StringDtype()
        _dtype_cls = pd.StringDtype
        _internal_fill_value = pd.NA

    arr = MyStringArray(
        values=np.array(["a", "b", "c"]), mask=np.array([False, True, False])
    )
    result = arr.to_numpy()
    expected = np.array(["a", pd.NA, "c"])
    tm.assert_numpy_array_equal(result, expected)


def test_to_numpy():
    arr = NumpyExtensionArray(np.array([1, 2, 3]))
    result = arr.to_numpy()
    assert result is arr._ndarray

    result = arr.to_numpy(copy=True)
    assert result is not arr._ndarray

    result = arr.to_numpy(dtype="f8")
    expected = np.array([1, 2, 3], dtype="f8")
    tm.assert_numpy_array_equal(result, expected)

