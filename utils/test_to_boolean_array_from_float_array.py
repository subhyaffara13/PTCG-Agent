
def test_to_boolean_array_from_float_array():
    result = pd.array(np.array([1.0, 0.0, 1.0, 0.0]), dtype="boolean")
    expected = pd.array([True, False, True, False], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

    # with missing values
    result = pd.array(np.array([1.0, 0.0, 1.0, np.nan]), dtype="boolean")
    expected = pd.array([True, False, True, None], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

