
def test_categorical_accessor(method):
    s = pd.Series(["a", "b"], dtype="category")
    s.attrs = {"a": 1}
    result = method(s.cat)
    assert result.attrs == {"a": 1}

