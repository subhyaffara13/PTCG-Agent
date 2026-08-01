
def test_has_varargs():
    assert has_varargs(lambda: None) is False
    assert has_varargs(lambda *args: None)
    assert has_varargs(lambda **kwargs: None) is False
    assert has_varargs(map)
    assert has_varargs(max) is None

