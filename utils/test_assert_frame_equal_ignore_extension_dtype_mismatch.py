
def test_assert_frame_equal_ignore_extension_dtype_mismatch():
    # https://github.com/pandas-dev/pandas/issues/35715
    left = DataFrame({"a": [1, 2, 3]}, dtype="Int64")
    right = DataFrame({"a": [1, 2, 3]}, dtype="Int32")
    tm.assert_frame_equal(left, right, check_dtype=False)

