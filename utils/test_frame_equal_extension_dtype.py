
def test_frame_equal_extension_dtype(frame_or_series, any_numeric_ea_dtype):
    # GH#39410
    obj = frame_or_series([1, 2], dtype=any_numeric_ea_dtype)
    tm.assert_equal(obj, obj, check_exact=True)

