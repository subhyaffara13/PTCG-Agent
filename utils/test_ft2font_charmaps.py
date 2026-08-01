
def test_ft2font_charmaps():
    def enc(name):
        # We don't expose the encoding enum from FreeType, but can generate it here.
        # For DejaVu, there are 5 charmaps, but only 2 have enum entries in FreeType.
        e = 0
        for x in name:
            e <<= 8
            e += ord(x)
        return e

    file = fm.findfont('DejaVu Sans')
    font = ft2font.FT2Font(file)
    assert font.num_charmaps == 5

    # Unicode.
    font.select_charmap(enc('unic'))
    unic = font.get_charmap()
    font.set_charmap(0)  # Unicode platform, Unicode BMP only.
    after = font.get_charmap()
    assert len(after) <= len(unic)
    for chr, glyph in after.items():
        assert unic[chr] == glyph == font.get_char_index(chr)
    font.set_charmap(1)  # Unicode platform, modern subtable.
    after = font.get_charmap()
    assert unic == after
    font.set_charmap(3)  # Windows platform, Unicode BMP only.
    after = font.get_charmap()
    assert len(after) <= len(unic)
    for chr, glyph in after.items():
        assert unic[chr] == glyph == font.get_char_index(chr)
    font.set_charmap(4)  # Windows platform, Unicode full repertoire, modern subtable.
    after = font.get_charmap()
    assert unic == after

    # This is just a random sample from FontForge.
    glyph_names = cast(dict[str, ft2font.GlyphIndexType], {
        'non-existent-glyph-name': 0,
        'plusminus': 115,
        'Racute': 278,
        'perthousand': 2834,
        'seveneighths': 3057,
        'triagup': 3721,
        'uni01D3': 405,
        'uni0417': 939,
        'uni2A02': 4464,
        'u1D305': 5410,
        'u1F0A1': 5784,
    })
    for name, index in glyph_names.items():
        assert font.get_name_index(name) == index
        if name == 'non-existent-glyph-name':
            name = '.notdef'
        # This doesn't always apply, but it does for DejaVu Sans.
        assert font.get_glyph_name(index) == name

    # Apple Roman.
    font.select_charmap(enc('armn'))
    armn = font.get_charmap()
    font.set_charmap(2)  # Macintosh platform, Roman.
    after = font.get_charmap()
    assert armn == after
    assert len(armn) <= 256  # 8-bit encoding.
    # The first 128 characters of Apple Roman match ASCII, which also matches Unicode.
    for o in range(1, 128):
        if o not in armn or o not in unic:
            continue
        assert unic[o] == armn[o]
    # Check a couple things outside the ASCII set that are different in each charset.
    examples = [
        # (Unicode, Macintosh)
        (0x2020, 0xA0),  # Dagger.
        (0x00B0, 0xA1),  # Degree symbol.
        (0x00A3, 0xA3),  # Pound sign.
        (0x00A7, 0xA4),  # Section sign.
        (0x00B6, 0xA6),  # Pilcrow.
        (0x221E, 0xB0),  # Infinity symbol.
    ]
    for u, m in examples:
        # Though the encoding is different, the glyph should be the same.
        assert unic[u] == armn[m]

    # Out-of-range charmap indices must be rejected rather than indexing out of
    # bounds. A negative index previously passed the upper-bound-only check and
    # read face->charmaps[i] out of bounds.
    with pytest.raises(RuntimeError, match='exceeds the available number'):
        font.set_charmap(-1)
    with pytest.raises(RuntimeError, match='exceeds the available number'):
        font.set_charmap(font.num_charmaps)

