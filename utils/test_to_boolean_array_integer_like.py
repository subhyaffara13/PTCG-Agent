
def test_to_boolean_array_integer_like():
    # integers of 0's and 1's
    result = pd.array([1, 0, 1, 0], dtype="boolean")
    expected = pd.array([True, False, True, False], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

    # with missing values
    result = pd.array([1, 0, 1, None], dtype="boolean")
    expected = pd.array([True, False, True, None], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

