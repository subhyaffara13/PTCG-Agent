
def reorderGlyphs(font: ttLib.TTFont, new_glyph_order: List[str]):
    old_glyph_order = font.getGlyphOrder()
    if len(new_glyph_order) != len(old_glyph_order):
        raise ValueError(
            f"New glyph order contains {len(new_glyph_order)} glyphs, "
            f"but font has {len(old_glyph_order)} glyphs"
        )

    if set(old_glyph_order) != set(new_glyph_order):
        raise ValueError(
            "New glyph order does not contain the same set of glyphs as the font:\n"
            f"* only in new: {set(new_glyph_order) - set(old_glyph_order)}\n"
            f"* only in old: {set(old_glyph_order) - set(new_glyph_order)}"
        )

    # Changing the order of glyphs in a TTFont requires that all tables that use
    # glyph indexes have been fully.
    # Cf. https://github.com/fonttools/fonttools/issues/2060
    font.ensureDecompiled()
    not_loaded = sorted(t for t in font.keys() if not font.isLoaded(t))
    if not_loaded:
        raise ValueError(f"Everything should be loaded, following aren't: {not_loaded}")

    font.setGlyphOrder(new_glyph_order)

    coverage_containers = {"GDEF", "GPOS", "GSUB", "MATH"}
    for tag in coverage_containers:
        if tag in font.keys():
            for path in _bfs_base_table(font[tag].table, f'font["{tag}"]'):
                value = path[-1].value
                reorder_key = (type(value), getattr(value, "Format", None))
                for reorder in _REORDER_RULES.get(reorder_key, []):
                    reorder.apply(font, value)

    for tag in ["CFF ", "CFF2"]:
        if tag in font:
            cff_table = font[tag]
            charstrings = cff_table.cff.topDictIndex[0].CharStrings.charStrings
            cff_table.cff.topDictIndex[0].charset = new_glyph_order
            cff_table.cff.topDictIndex[0].CharStrings.charStrings = {
                k: charstrings.get(k) for k in new_glyph_order
            }

