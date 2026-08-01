
def test_bytearray_to_string():
    """Tests the ability to pass bytearray to C++ string-accepting functions"""
    assert m.string_length(bytearray(b"Hi")) == 2
    assert m.strlen(bytearray(b"bytearray")) == 9
    assert m.string_length(bytearray()) == 0
    assert m.string_length(bytearray("🦜", "utf-8", "strict")) == 4
    assert m.string_length(bytearray(b"\x80")) == 1

