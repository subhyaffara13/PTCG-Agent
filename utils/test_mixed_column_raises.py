
def test_mixed_column_raises(df, method, using_infer_string):
    # GH 16832
    if method == "sum":
        msg = r'can only concatenate str \(not "int"\) to str|does not support'
    else:
        msg = "not supported between instances of 'str' and 'float'"
    if not using_infer_string:
        with pytest.raises(TypeError, match=msg):
            getattr(df, method)()
    else:
        getattr(df, method)()

