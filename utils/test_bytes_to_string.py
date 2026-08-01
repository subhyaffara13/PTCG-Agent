
def test_bytes_to_string():
    """Tests the ability to pass bytes to C++ string-accepting functions.  Note that this is
    one-way: the only way to return bytes to Python is via the pybind11::bytes class."""
    # Issue #816

    assert m.strlen(b"hi") == 2
    assert m.string_length(b"world") == 5
    assert m.string_length(b"a\x00b") == 3
    assert m.strlen(b"a\x00b") == 1  # C-string limitation

    # passing in a utf8 encoded string should work
    assert m.string_length("💩".encode()) == 4

