
def test_split_blank_string(any_string_dtype):
    # expand blank split GH 20067
    values = Series([""], name="test", dtype=any_string_dtype)
    result = values.str.split(expand=True)
    exp = DataFrame([[]], dtype=any_string_dtype)  # NOTE: this is NOT an empty df
    tm.assert_frame_equal(result, exp)

