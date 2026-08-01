
def _serialize_type42(font, subset_index, subset, fontdata):
    """
    Output a PostScript Type-42 format representation of font

    Parameters
    ----------
    font : fontTools.ttLib.ttFont.TTFont
        The original font object
    subset_index : int
        The subset of the above font to be created.
    subset : fontTools.ttLib.ttFont.TTFont
        The subset font object
    fontdata : bytes
        The raw font data in TTF format

    Returns
    -------
    str
        The Type-42 formatted font
    """
    version, breakpoints = _version_and_breakpoints(font.get('loca'), fontdata)
    post = font['post']
    name = font['name']
    chars = _generate_charstrings(subset)
    sfnts = _generate_sfnts(fontdata, subset, breakpoints)
    return textwrap.dedent(f"""
        %%!PS-TrueTypeFont-{version[0]}.{version[1]}-{font['head'].fontRevision:.7f}
        10 dict begin
        /FontType 42 def
        /FontMatrix [1 0 0 1 0 0] def
        /FontName /{name.getDebugName(6)}-{subset_index} def
        /FontInfo 7 dict dup begin
        /FullName ({name.getDebugName(4)}) def
        /FamilyName ({name.getDebugName(1)}) def
        /Version ({name.getDebugName(5)}) def
        /ItalicAngle {post.italicAngle} def
        /isFixedPitch {'true' if post.isFixedPitch else 'false'} def
        /UnderlinePosition {post.underlinePosition} def
        /UnderlineThickness {post.underlineThickness} def
        end readonly def
        /Encoding StandardEncoding def
        /FontBBox [{_nums_to_str(*_bounds(font))}] def
        /PaintType 0 def
        /CIDMap 0 def
        {chars}
        {sfnts}
        FontName currentdict end definefont pop
        """)

