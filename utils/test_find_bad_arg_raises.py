
def test_find_bad_arg_raises(any_string_dtype):
    ser = Series([], dtype=any_string_dtype)
    with pytest.raises(TypeError, match="expected a string object, not int"):
        ser.str.find(0)

    with pytest.raises(TypeError, match="expected a string object, not int"):
        ser.str.rfind(0)

