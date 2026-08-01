
def test_to_boolean_array_all_none():
    expected = BooleanArray(np.array([True, True, True]), np.array([True, True, True]))

    result = pd.array([None, None, None], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)
    result = pd.array(np.array([None, None, None], dtype=object), dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

