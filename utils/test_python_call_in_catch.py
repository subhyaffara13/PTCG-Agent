
def test_python_call_in_catch():
    d = {}
    assert m.python_call_in_destructor(d) is True
    assert d["good"] is True

