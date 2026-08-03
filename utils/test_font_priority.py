from pathlib import Path


def test_font_priority():
    with rc_context(rc={
            'font.sans-serif':
            ['cmmi10', 'Bitstream Vera Sans']}):
        fontfile = findfont(FontProperties(family=["sans-serif"]))
    assert Path(fontfile).name == 'cmmi10.ttf'

    # Smoketest get_charmap, which isn't used internally anymore
    font = get_font(fontfile)
    cmap = font.get_charmap()
    assert len(cmap) == 131
    assert cmap[8729] == 30

