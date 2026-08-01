
def test_addfont_as_path(monkeypatch):
    """Smoke test that addfont() accepts pathlib.Path."""
    font_test_file = 'mpltest.ttf'
    path = Path(__file__).parent / 'data' / font_test_file
    try:
        fontManager.addfont(path)
        assert fontManager.findfont('mpltest:weight=500') == FontPath(path, 0)
        with monkeypatch.context() as m, pytest.raises(ValueError):
            m.setenv('MPL_IGNORE_SYSTEM_FONTS', 'true')  # Can only find internal fonts.
            fontManager.findfont('mpltest:weight=500', fallback_to_default=False)
        added, = (font for font in fontManager.ttflist
                  if font.fname.endswith(font_test_file))
        fontManager.ttflist.remove(added)
    finally:
        to_remove = [font for font in fontManager.ttflist
                     if font.fname.endswith(font_test_file)]
        for font in to_remove:
            fontManager.ttflist.remove(font)

