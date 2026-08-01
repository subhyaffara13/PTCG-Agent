
def test_single_char_arguments():
    """Tests failures for passing invalid inputs to char-accepting functions"""

    def toobig_message(r):
        return f"Character code point not in range({r:#x})"

    toolong_message = "Expected a character, but multi-character string found"

    assert m.ord_char("a") == 0x61  # simple ASCII
    assert m.ord_char_lv("b") == 0x62
    assert (
        m.ord_char("é") == 0xE9
    )  # requires 2 bytes in utf-8, but can be stuffed in a char
    with pytest.raises(ValueError) as excinfo:
        assert m.ord_char("Ā") == 0x100  # requires 2 bytes, doesn't fit in a char
    assert str(excinfo.value) == toobig_message(0x100)
    with pytest.raises(ValueError) as excinfo:
        assert m.ord_char("ab")
    assert str(excinfo.value) == toolong_message

    assert m.ord_char16("a") == 0x61
    assert m.ord_char16("é") == 0xE9
    assert m.ord_char16_lv("ê") == 0xEA
    assert m.ord_char16("Ā") == 0x100
    assert m.ord_char16("‽") == 0x203D
    assert m.ord_char16("♥") == 0x2665
    assert m.ord_char16_lv("♡") == 0x2661
    with pytest.raises(ValueError) as excinfo:
        assert m.ord_char16("🎂") == 0x1F382  # requires surrogate pair
    assert str(excinfo.value) == toobig_message(0x10000)
    with pytest.raises(ValueError) as excinfo:
        assert m.ord_char16("aa")
    assert str(excinfo.value) == toolong_message

    assert m.ord_char32("a") == 0x61
    assert m.ord_char32("é") == 0xE9
    assert m.ord_char32("Ā") == 0x100
    assert m.ord_char32("‽") == 0x203D
    assert m.ord_char32("♥") == 0x2665
    assert m.ord_char32("🎂") == 0x1F382
    with pytest.raises(ValueError) as excinfo:
        assert m.ord_char32("aa")
    assert str(excinfo.value) == toolong_message

    assert m.ord_wchar("a") == 0x61
    assert m.ord_wchar("é") == 0xE9
    assert m.ord_wchar("Ā") == 0x100
    assert m.ord_wchar("‽") == 0x203D
    assert m.ord_wchar("♥") == 0x2665
    if m.wchar_size == 2:
        with pytest.raises(ValueError) as excinfo:
            assert m.ord_wchar("🎂") == 0x1F382  # requires surrogate pair
        assert str(excinfo.value) == toobig_message(0x10000)
    else:
        assert m.ord_wchar("🎂") == 0x1F382
    with pytest.raises(ValueError) as excinfo:
        assert m.ord_wchar("aa")
    assert str(excinfo.value) == toolong_message

    if hasattr(m, "has_u8string"):
        assert m.ord_char8("a") == 0x61  # simple ASCII
        assert m.ord_char8_lv("b") == 0x62
        assert (
            m.ord_char8("é") == 0xE9
        )  # requires 2 bytes in utf-8, but can be stuffed in a char
        with pytest.raises(ValueError) as excinfo:
            assert m.ord_char8("Ā") == 0x100  # requires 2 bytes, doesn't fit in a char
        assert str(excinfo.value) == toobig_message(0x100)
        with pytest.raises(ValueError) as excinfo:
            assert m.ord_char8("ab")
        assert str(excinfo.value) == toolong_message

