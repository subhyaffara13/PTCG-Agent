
def test_assert_frame_equal_datetime_like_dtype_mismatch(dtype):
    df1 = DataFrame({"a": []}, dtype=dtype)
    df2 = DataFrame({"a": []})
    tm.assert_frame_equal(df1, df2, check_dtype=False)

