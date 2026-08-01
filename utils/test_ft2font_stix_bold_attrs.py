
def test_ft2font_stix_bold_attrs():
    file = fm.findfont('STIXSizeTwoSym:bold')
    font = ft2font.FT2Font(file)
    assert font.fname == file
    # Names extracted from FontForge: Font Information → PS Names tab.
    assert font.postscript_name == 'STIXSizeTwoSym-Bold'
    assert font.family_name == 'STIXSizeTwoSym'
    assert font.style_name == 'Bold'
    assert font.num_faces == 1  # Single TTF.
    assert font.num_named_instances == 0  # Not a variable font.
    assert font.num_glyphs == 20  # From compact encoding view in FontForge.
    assert font.num_fixed_sizes == 0  # All glyphs are scalable.
    assert font.num_charmaps == 3
    # Other internal flags are set, so only check the ones we're allowed to test.
    expected_flags = (ft2font.FaceFlags.SCALABLE | ft2font.FaceFlags.SFNT |
                      ft2font.FaceFlags.HORIZONTAL | ft2font.FaceFlags.GLYPH_NAMES)
    assert expected_flags in font.face_flags
    assert font.style_flags == ft2font.StyleFlags.BOLD
    assert font.scalable
    # From FontForge: Font Information → General tab → entry name below.
    assert font.units_per_EM == 1000  # Em Size.
    assert font.underline_position == -133  # Underline position.
    assert font.underline_thickness == 20  # Underline height.
    # From FontForge: Font Information → OS/2 tab → Metrics tab → entry name below.
    assert font.ascender == 2095  # HHead Ascent.
    assert font.descender == -404  # HHead Descent.
    # Unconfirmed values.
    assert font.height == 2499
    assert font.max_advance_width == 1130
    assert font.max_advance_height == 2499
    assert font.bbox == (4, -355, 1185, 2095)

