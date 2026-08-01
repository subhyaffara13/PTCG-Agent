
def test_str_replace_unsupported(arg_name, arg):
    ser = pd.Series(["abc", None], dtype=ArrowDtype(pa.string()))
    kwargs = {"pat": "b", "repl": "x", "regex": True}
    kwargs[arg_name] = arg
    with pytest.raises(NotImplementedError, match="replace is not supported"):
        ser.str.replace(**kwargs)

