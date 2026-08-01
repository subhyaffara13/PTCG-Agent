
def test_setitem_no_coercion():
    # https://github.com/pandas-dev/pandas/issues/28150
    arr = NumpyExtensionArray(np.array([1, 2, 3]))
    with pytest.raises(ValueError, match="int"):
        arr[0] = "a"

    # With a value that we do coerce, check that we coerce the value
    #  and not the underlying array.
    arr[0] = 2.5
    assert isinstance(arr[0], (int, np.integer)), type(arr[0])

