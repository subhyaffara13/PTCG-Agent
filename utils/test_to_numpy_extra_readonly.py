
def test_to_numpy_extra_readonly(arr):
    arr[0] = NaT
    original = arr.copy()
    arr._readonly = True

    result = arr.to_numpy(dtype=object)
    assert result.flags.writeable

    # numpy does not do zero-copy conversion from M8 to i8
    result = arr.to_numpy(dtype="int64")
    assert result.flags.writeable

    tm.assert_equal(arr, original)

