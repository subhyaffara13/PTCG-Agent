
def test_pad_width_bad_arg_raises(method_name, any_string_dtype):
    # see gh-13598
    s = Series(["1", "22", "a", "bb"], dtype=any_string_dtype)
    op = operator.methodcaller(method_name, "f")

    msg = "width must be of integer type, not str"
    with pytest.raises(TypeError, match=msg):
        op(s.str)

