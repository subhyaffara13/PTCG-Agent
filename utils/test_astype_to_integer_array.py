
def test_astype_to_integer_array():
    # astype to IntegerArray
    arr = pd.array([True, False, None], dtype="boolean")

    result = arr.astype("Int64")
    expected = pd.array([1, 0, None], dtype="Int64")
    tm.assert_extension_array_equal(result, expected)


def test_astype_to_integer_array():
    # astype to IntegerArray
    arr = pd.array([0.0, 1.5, None], dtype="Float64")

    result = arr.astype("Int64")
    expected = pd.array([0, 1, None], dtype="Int64")
    tm.assert_extension_array_equal(result, expected)

