
def test_pad_fillchar_bad_arg_raises(any_string_dtype):
    s = Series(["a", "b", np.nan, "c", np.nan, "eeeeee"], dtype=any_string_dtype)

    msg = "fillchar must be a character, not str"
    with pytest.raises(TypeError, match=msg):
        s.str.pad(5, fillchar="XY")

    msg = "fillchar must be a character, not int"
    with pytest.raises(TypeError, match=msg):
        s.str.pad(5, fillchar=5)

