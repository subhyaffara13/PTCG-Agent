
def test_unicode_conversion():
    """Tests unicode conversion and error reporting."""
    assert m.good_utf8_string() == "Say utf8‽ 🎂 𝐀"
    assert m.good_utf16_string() == "b‽🎂𝐀z"
    assert m.good_utf32_string() == "a𝐀🎂‽z"
    assert m.good_wchar_string() == "a⸘𝐀z"
    if hasattr(m, "has_u8string"):
        assert m.good_utf8_u8string() == "Say utf8‽ 🎂 𝐀"

    with pytest.raises(UnicodeDecodeError):
        m.bad_utf8_string()

    with pytest.raises(UnicodeDecodeError):
        m.bad_utf16_string()

    # These are provided only if they actually fail (they don't when 32-bit)
    if hasattr(m, "bad_utf32_string"):
        with pytest.raises(UnicodeDecodeError):
            m.bad_utf32_string()
    if hasattr(m, "bad_wchar_string"):
        with pytest.raises(UnicodeDecodeError):
            m.bad_wchar_string()
    if hasattr(m, "has_u8string"):
        with pytest.raises(UnicodeDecodeError):
            m.bad_utf8_u8string()

    assert m.u8_Z() == "Z"
    assert m.u8_eacute() == "é"
    assert m.u16_ibang() == "‽"
    assert m.u32_mathbfA() == "𝐀"
    assert m.wchar_heart() == "♥"
    if hasattr(m, "has_u8string"):
        assert m.u8_char8_Z() == "Z"

