
def test_astype_boolean():
    # https://github.com/pandas-dev/pandas/issues/31102
    a = pd.array([1, 0, -1, 2, None], dtype="Int64")
    result = a.astype("boolean")
    expected = pd.array([True, False, True, True, None], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)

