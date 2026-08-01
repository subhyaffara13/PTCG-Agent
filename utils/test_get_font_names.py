
def test_get_font_names():
    paths_mpl = [cbook._get_data_path('fonts', subdir) for subdir in ['ttf']]
    fonts_mpl = findSystemFonts(paths_mpl, fontext='ttf')
    fonts_system = findSystemFonts(fontext='ttf')
    ttf_fonts = set()
    for path in fonts_mpl + fonts_system:
        try:
            font = ft2font.FT2Font(path)
            prop = ttfFontProperty(font)
            ttf_fonts.add(prop.name)
            for face_index in range(1, font.num_faces):
                font = ft2font.FT2Font(path, face_index=face_index)
                prop = ttfFontProperty(font)
                ttf_fonts.add(prop.name)
        except Exception:
            pass
    # fontManager may contain additional entries for alternative family names
    # (e.g. typographic family, platform-specific Name ID 1) registered by
    # addfont(), so primary names must be a subset of the manager's names.
    assert ttf_fonts <= set(fontManager.get_font_names())

