
def test_str_accessor_no_new_attributes(any_string_dtype):
    # https://github.com/pandas-dev/pandas/issues/10673
    ser = Series(list("aabbcde"), dtype=any_string_dtype)
    with pytest.raises(AttributeError, match="You cannot add any new attribute"):
        ser.str.xlabel = "a"

