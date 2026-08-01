
def test_integer_array_from_boolean():
    # GH31104
    expected = pd.array(np.array([True, False]), dtype="Int64")
    result = pd.array(np.array([True, False], dtype=object), dtype="Int64")
    tm.assert_extension_array_equal(result, expected)

