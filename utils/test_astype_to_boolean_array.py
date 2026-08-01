
def test_astype_to_boolean_array():
    # astype to BooleanArray
    arr = pd.array([True, False, None], dtype="boolean")

    result = arr.astype("boolean")
    tm.assert_extension_array_equal(result, arr)
    result = arr.astype(pd.BooleanDtype())
    tm.assert_extension_array_equal(result, arr)


def test_astype_to_boolean_array():
    # astype to BooleanArray
    arr = pd.array([0.0, 1.0, None], dtype="Float64")

    result = arr.astype("boolean")
    expected = pd.array([False, True, None], dtype="boolean")
    tm.assert_extension_array_equal(result, expected)
    result = arr.astype(pd.BooleanDtype())
    tm.assert_extension_array_equal(result, expected)

