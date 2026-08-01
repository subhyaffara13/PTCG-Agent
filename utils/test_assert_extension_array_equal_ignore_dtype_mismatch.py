
def test_assert_extension_array_equal_ignore_dtype_mismatch(any_int_dtype):
    # https://github.com/pandas-dev/pandas/issues/35715
    left = array([1, 2, 3], dtype="Int64")
    right = array([1, 2, 3], dtype=any_int_dtype)
    tm.assert_extension_array_equal(left, right, check_dtype=False)

