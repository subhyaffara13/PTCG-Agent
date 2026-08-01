
def test_replace_wrong_repl_type_raises(any_string_dtype, index_or_series, repl, data):
    # https://github.com/pandas-dev/pandas/issues/13438
    msg = "repl must be a string or callable"
    obj = index_or_series(data, dtype=any_string_dtype)
    with pytest.raises(TypeError, match=msg):
        obj.str.replace("a", repl)

