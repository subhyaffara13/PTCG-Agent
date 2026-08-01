
def getfd_map(varFont, fonts_list):
    """Since a subset source font may have fewer FontDicts in their
    FDArray than the default font, we have to match up the FontDicts in
    the different fonts . We do this with the FDSelect array, and by
    assuming that the same glyph will reference  matching FontDicts in
    each source font. We return a mapping from fdIndex in the default
    font to a dictionary which maps each master list index of each
    region font to the equivalent fdIndex in the region font."""
    fd_map = {}
    default_font = fonts_list[0]
    region_fonts = fonts_list[1:]
    num_regions = len(region_fonts)
    topDict = _cff_or_cff2(default_font).cff.topDictIndex[0]
    if not hasattr(topDict, "FDSelect"):
        # All glyphs reference only one FontDict.
        # Map the FD index for regions to index 0.
        fd_map[0] = {ri: 0 for ri in range(num_regions)}
        return fd_map

    gname_mapping = {}
    default_fdSelect = topDict.FDSelect
    glyphOrder = default_font.getGlyphOrder()
    for gid, fdIndex in enumerate(default_fdSelect):
        gname_mapping[glyphOrder[gid]] = fdIndex
        if fdIndex not in fd_map:
            fd_map[fdIndex] = {}
    for ri, region_font in enumerate(region_fonts):
        region_glyphOrder = region_font.getGlyphOrder()
        region_topDict = _cff_or_cff2(region_font).cff.topDictIndex[0]
        if not hasattr(region_topDict, "FDSelect"):
            # All the glyphs share the same FontDict. Pick any glyph.
            default_fdIndex = gname_mapping[region_glyphOrder[0]]
            fd_map[default_fdIndex][ri] = 0
        else:
            region_fdSelect = region_topDict.FDSelect
            for gid, fdIndex in enumerate(region_fdSelect):
                default_fdIndex = gname_mapping[region_glyphOrder[gid]]
                region_map = fd_map[default_fdIndex]
                if ri not in region_map:
                    region_map[ri] = fdIndex
    return fd_map

