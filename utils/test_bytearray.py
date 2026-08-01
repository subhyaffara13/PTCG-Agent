
def test_bytearray():
    assert m.bytearray_from_char_ssize_t().decode() == "$%"
    assert m.bytearray_from_char_size_t().decode() == "@$!"
    assert m.bytearray_from_string().decode() == "foo"
    assert m.bytearray_size() == len("foo")

