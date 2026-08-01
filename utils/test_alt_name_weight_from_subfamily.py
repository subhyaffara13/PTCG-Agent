
def test_alt_name_weight_from_subfamily(subfam, expected):
    """_get_font_alt_names derives weight from the paired subfamily string."""
    ms_key = (3, 1, 0x0409)
    fake_font = MagicMock()
    fake_font.get_sfnt.return_value = {
        (*ms_key, 1): "Family Alt".encode("utf-16-be"),
        (*ms_key, 2): subfam.encode("utf-16-be"),
    }
    result = _get_font_alt_names(fake_font, "Family")
    assert result == [("Family Alt", expected)]

