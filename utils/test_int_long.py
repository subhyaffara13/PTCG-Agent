
def test_int_long():
    assert isinstance(m.int_cast(), int)
    assert isinstance(m.long_cast(), int)
    assert isinstance(m.longlong_cast(), int)

