
def test_string_view(capture):
    """Tests support for C++17 string_view arguments and return values"""
    assert m.string_view_chars("Hi") == [72, 105]
    assert m.string_view_chars("Hi 🎂") == [72, 105, 32, 0xF0, 0x9F, 0x8E, 0x82]
    assert m.string_view16_chars("Hi 🎂") == [72, 105, 32, 0xD83C, 0xDF82]
    assert m.string_view32_chars("Hi 🎂") == [72, 105, 32, 127874]
    if hasattr(m, "has_u8string"):
        assert m.string_view8_chars("Hi") == [72, 105]
        assert m.string_view8_chars("Hi 🎂") == [72, 105, 32, 0xF0, 0x9F, 0x8E, 0x82]

    assert m.string_view_return() == "utf8 secret 🎂"
    assert m.string_view16_return() == "utf16 secret 🎂"
    assert m.string_view32_return() == "utf32 secret 🎂"
    if hasattr(m, "has_u8string"):
        assert m.string_view8_return() == "utf8 secret 🎂"

    with capture:
        m.string_view_print("Hi")
        m.string_view_print("utf8 🎂")
        m.string_view16_print("utf16 🎂")
        m.string_view32_print("utf32 🎂")
    assert (
        capture
        == """
        Hi 2
        utf8 🎂 9
        utf16 🎂 8
        utf32 🎂 7
    """
    )
    if hasattr(m, "has_u8string"):
        with capture:
            m.string_view8_print("Hi")
            m.string_view8_print("utf8 🎂")
        assert (
            capture
            == """
            Hi 2
            utf8 🎂 9
        """
        )

    with capture:
        m.string_view_print("Hi, ascii")
        m.string_view_print("Hi, utf8 🎂")
        m.string_view16_print("Hi, utf16 🎂")
        m.string_view32_print("Hi, utf32 🎂")
    assert (
        capture
        == """
        Hi, ascii 9
        Hi, utf8 🎂 13
        Hi, utf16 🎂 12
        Hi, utf32 🎂 11
    """
    )
    if hasattr(m, "has_u8string"):
        with capture:
            m.string_view8_print("Hi, ascii")
            m.string_view8_print("Hi, utf8 🎂")
        assert (
            capture
            == """
            Hi, ascii 9
            Hi, utf8 🎂 13
        """
        )

    assert m.string_view_bytes() == b"abc \x80\x80 def"
    assert m.string_view_str() == "abc ‽ def"
    assert m.string_view_from_bytes("abc ‽ def".encode()) == "abc ‽ def"
    if hasattr(m, "has_u8string"):
        assert m.string_view8_str() == "abc ‽ def"
    assert m.string_view_memoryview() == "Have some 🎂".encode()

    assert m.bytes_from_type_with_both_operator_string_and_string_view() == b"success"
    assert m.str_from_type_with_both_operator_string_and_string_view() == "success"

