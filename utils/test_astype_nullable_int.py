
def test_astype_nullable_int(dtype):
    arr = pd.array(["1", pd.NA, "3"], dtype=dtype)

    result = arr.astype("Int64")
    expected = pd.array([1, pd.NA, 3], dtype="Int64")
    tm.assert_extension_array_equal(result, expected)

