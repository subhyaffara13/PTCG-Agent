
def test_coerce_to_numpy_array():
    # with missing values -> object dtype
    arr = pd.array([True, False, None], dtype="boolean")
    result = np.array(arr)
    expected = np.array([True, False, pd.NA], dtype="object")
    tm.assert_numpy_array_equal(result, expected)

    # also with no missing values -> object dtype
    arr = pd.array([True, False, True], dtype="boolean")
    result = np.array(arr)
    expected = np.array([True, False, True], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)

    # force bool dtype
    result = np.array(arr, dtype="bool")
    expected = np.array([True, False, True], dtype="bool")
    tm.assert_numpy_array_equal(result, expected)
    # with missing values will raise error
    arr = pd.array([True, False, None], dtype="boolean")
    msg = (
        "cannot convert to 'bool'-dtype NumPy array with missing values. "
        "Specify an appropriate 'na_value' for this dtype."
    )
    with pytest.raises(ValueError, match=msg):
        np.array(arr, dtype="bool")

