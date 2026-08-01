
def _generate_charstrings(font):
    """
    Transform font glyphs into CharStrings

    Helper function for _font_to_ps_type42.

    Parameters
    ----------
    font : fontTools.ttLib.ttFont.TTFont
        The font

    Returns
    -------
    str
        A definition of the CharStrings dictionary in PostScript
    """
    go = font.getGlyphOrder()
    s = f'/CharStrings {len(go)} dict dup begin\n'
    for i, name in enumerate(go):
        s += f'/{name} {i} def\n'
    s += 'end readonly def'
    return s

