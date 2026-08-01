
def test_addfont_alternative_names(tmp_path):
    """
    Fonts that advertise different family names across platforms or name IDs
    should be registered under all of those names so users can address the font
    by any of them.

    Two real-world patterns are covered:

    - **MS platform ID 1 differs from Mac platform ID 1** (e.g. Ubuntu Light):
      FreeType returns the Mac ID 1 value as ``family_name``; the MS ID 1
      value ("Ubuntu Light") is an equally valid name that users expect to work.
    - **Name ID 16 (Typographic Family) differs from ID 1** (older fonts):
      some fonts store a broader family name in ID 16.
    """
    mac_key = (1, 0, 0)
    ms_key = (3, 1, 0x0409)

    # Case 1: MS ID1 differs from Mac ID1 (Ubuntu Light pattern)
    # Mac ID1="Test Family" → FreeType family_name (primary)
    # MS  ID1="Test Family Light" → alternate name users expect to work
    ubuntu_style_sfnt = {
        (*mac_key, 1): "Test Family".encode("latin-1"),
        (*ms_key,  1): "Test Family Light".encode("utf-16-be"),
        (*mac_key, 2): "Light".encode("latin-1"),
        (*ms_key,  2): "Regular".encode("utf-16-be"),
    }
    fake_font = MagicMock()
    fake_font.get_sfnt.return_value = ubuntu_style_sfnt

    assert _get_font_alt_names(fake_font, "Test Family") == [("Test Family Light", 400)]
    assert _get_font_alt_names(fake_font, "Test Family Light") == [
        ("Test Family", 300)]

    # Case 2: ID 16 differs from ID 1 (older typographic-family pattern)
    # ID 17 (typographic subfamily) is absent → defaults to weight 400
    id16_sfnt = {
        (*mac_key, 1):  "Test Family".encode("latin-1"),
        (*ms_key,  1):  "Test Family".encode("utf-16-be"),
        (*ms_key,  16): "Test Family Light".encode("utf-16-be"),
    }
    fake_font_id16 = MagicMock()
    fake_font_id16.get_sfnt.return_value = id16_sfnt

    assert _get_font_alt_names(
        fake_font_id16, "Test Family"
    ) == [("Test Family Light", 400)]

    # Case 3: all entries agree → no alternates
    same_sfnt = {
        (*mac_key, 1): "Test Family".encode("latin-1"),
        (*ms_key,  1): "Test Family".encode("utf-16-be"),
    }
    fake_font_same = MagicMock()
    fake_font_same.get_sfnt.return_value = same_sfnt
    assert _get_font_alt_names(fake_font_same, "Test Family") == []

    # Case 4: get_sfnt() raises ValueError (e.g. non-SFNT font) → empty list
    fake_font_no_sfnt = MagicMock()
    fake_font_no_sfnt.get_sfnt.side_effect = ValueError
    assert _get_font_alt_names(fake_font_no_sfnt, "Test Family") == []

    fake_path = str(tmp_path / "fake.ttf")
    primary_entry = FontEntry(fname=fake_path, name="Test Family",
                              style="normal", variant="normal",
                              weight=300, stretch="normal", size="scalable")

    with patch("matplotlib.font_manager.ft2font.FT2Font",
               return_value=fake_font), \
         patch("matplotlib.font_manager.ttfFontProperty",
               return_value=primary_entry):
        fm_instance = fm_mod.FontManager.__new__(fm_mod.FontManager)
        fm_instance.ttflist = []
        fm_instance.afmlist = []
        fm_instance._findfont_cached = MagicMock()
        fm_instance._findfont_cached.cache_clear = MagicMock()
        fm_instance.addfont(fake_path)

    names = [e.name for e in fm_instance.ttflist]
    assert names == ["Test Family", "Test Family Light"]
    alt_entry = fm_instance.ttflist[1]
    assert alt_entry.weight == 400
    assert alt_entry.style == primary_entry.style
    assert alt_entry.fname == primary_entry.fname

