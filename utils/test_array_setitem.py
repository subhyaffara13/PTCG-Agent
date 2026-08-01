
def test_array_setitem():
    # GH 31446
    arr = pd.array([1, 2], dtype="Int64")
    arr[arr > 1] = 1

    expected = pd.array([1, 1], dtype="Int64")
    tm.assert_extension_array_equal(arr, expected)

