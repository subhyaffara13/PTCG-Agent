
def test_downcast_nullable_mask_is_copied():
    # GH38974

    arr = pd.array([1, 2, pd.NA], dtype="Int64")

    result = to_numeric(arr, downcast="integer")
    expected = pd.array([1, 2, pd.NA], dtype="Int8")
    tm.assert_extension_array_equal(result, expected)

    arr[1] = pd.NA  # should not modify result
    tm.assert_extension_array_equal(result, expected)

