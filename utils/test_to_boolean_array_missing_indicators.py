
def test_to_boolean_array_missing_indicators(a, b):
    result = pd.array(a, dtype="boolean")
    expected = pd.array(b, dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

