
def test_replace_literal_callable_raises(any_string_dtype):
    ser = Series([], dtype=any_string_dtype)
    repl = lambda m: m.group(0).swapcase()

    msg = "Cannot use a callable replacement when regex=False"
    with pytest.raises(ValueError, match=msg):
        ser.str.replace("abc", repl, regex=False)

