
def test_user_fonts_linux(tmpdir, monkeypatch):
    font_test_file = 'mpltest.ttf'

    # Precondition: the test font should not be available
    fonts = findSystemFonts()
    if any(font_test_file in font for font in fonts):
        pytest.skip(f'{font_test_file} already exists in system fonts')

    # Prepare a temporary user font directory
    user_fonts_dir = tmpdir.join('fonts')
    user_fonts_dir.ensure(dir=True)
    shutil.copyfile(Path(__file__).parent / 'data' / font_test_file,
                    user_fonts_dir.join(font_test_file))

    with monkeypatch.context() as m:
        m.setenv('XDG_DATA_HOME', str(tmpdir))
        _get_fontconfig_fonts.cache_clear()
        # Now, the font should be available
        fonts = findSystemFonts()
        assert any(font_test_file in font for font in fonts)

    # Make sure the temporary directory is no longer cached.
    _get_fontconfig_fonts.cache_clear()

