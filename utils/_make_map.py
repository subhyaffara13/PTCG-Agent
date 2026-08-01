
def _make_map(font, chars, gids):
    assert len(chars) == len(gids)
    glyphNames = font.getGlyphNameMany(gids)
    cmap = {}
    for char, gid, name in zip(chars, gids, glyphNames):
        if gid == 0:
            continue
        cmap[char] = name
    return cmap

