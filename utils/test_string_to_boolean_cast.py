
def test_string_to_boolean_cast(dtype, out_dtype):
    # Only the last two (empty) strings are falsy (the `\0` is stripped):
    arr = np.array(
            ["10", "10\0\0\0", "0\0\0", "0", "False", " ", "", "\0"],
            dtype=dtype)
    expected = np.array(
            [True, True, True, True, True, True, False, False],
            dtype=out_dtype)
    assert_array_equal(arr.astype(out_dtype), expected)
    # As it's similar, check that nonzero behaves the same (structs are
    # nonzero if all entries are)
    assert_array_equal(np.nonzero(arr), np.nonzero(expected))

