
def test_ft2font_cm_attrs():
    file = fm.findfont('cmtt10')
    font = ft2font.FT2Font(file)
    assert font.fname == file
    # Names extracted from FontForge: Font Information → PS Names tab.
    assert font.postscript_name == 'Cmtt10'
    assert font.family_name == 'cmtt10'
    assert font.style_name == 'Regular'
    assert font.num_faces == 1  # Single TTF.
    assert font.num_named_instances == 0  # Not a variable font.
    assert font.num_glyphs == 133  # From compact encoding view in FontForge.
    assert font.num_fixed_sizes == 0  # All glyphs are scalable.
    assert font.num_charmaps == 2
    # Other internal flags are set, so only check the ones we're allowed to test.
    expected_flags = (ft2font.FaceFlags.SCALABLE | ft2font.FaceFlags.SFNT |
                      ft2font.FaceFlags.HORIZONTAL | ft2font.FaceFlags.GLYPH_NAMES)
    assert expected_flags in font.face_flags
    assert font.style_flags == ft2font.StyleFlags.NORMAL
    assert font.scalable
    # From FontForge: Font Information → General tab → entry name below.
    assert font.units_per_EM == 2048  # Em Size.
    assert font.underline_position == -143  # Underline position.
    assert font.underline_thickness == 20  # Underline height.
    # From FontForge: Font Information → OS/2 tab → Metrics tab → entry name below.
    assert font.ascender == 1276  # HHead Ascent.
    assert font.descender == -489  # HHead Descent.
    # Unconfirmed values.
    assert font.height == 1765
    assert font.max_advance_width == 1536
    assert font.max_advance_height == 1765
    assert font.bbox == (-12, -477, 1280, 1430)

