
def test_string_method(method):
    s = pd.Series(["a1"])
    s.attrs = {"a": 1}
    result = method(s.str)
    assert result.attrs == {"a": 1}

