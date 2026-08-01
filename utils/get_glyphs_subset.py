
def get_glyphs_subset(fontfile: FontPath, glyphs: set[GlyphIndexType]) -> TTFont:
    """
    Subset a TTF font.

    Reads the named fontfile and restricts the font to the glyphs.

    Parameters
    ----------
    fontfile : FontPath
        Path to the font file
    glyphs : set[GlyphIndexType]
        Set of glyph indices to include in subset.

    Returns
    -------
    fontTools.ttLib.ttFont.TTFont
        An open font object representing the subset, which needs to
        be closed by the caller.
    """
    options = subset.Options(glyph_names=True, recommended_glyphs=True,
                             retain_gids=True)

    # Prevent subsetting extra tables.
    options.drop_tables += [
        'FFTM',  # FontForge Timestamp.
        'PfEd',  # FontForge personal table.
        'BDF',  # X11 BDF header.
        'meta',  # Metadata stores design/supported languages (meaningless for subsets).
        'MERG',  # Merge Table.
        'TSIV',  # Microsoft Visual TrueType extension.
        'Zapf',  # Information about the individual glyphs in the font.
        'bdat',  # The bitmap data table.
        'bloc',  # The bitmap location table.
        'cidg',  # CID to Glyph ID table (Apple Advanced Typography).
        'fdsc',  # The font descriptors table.
        'feat',  # Feature name table (Apple Advanced Typography).
        'fmtx',  # The Font Metrics Table.
        'fond',  # Data-fork font information (Apple Advanced Typography).
        'just',  # The justification table (Apple Advanced Typography).
        'kerx',  # An extended kerning table (Apple Advanced Typography).
        'ltag',  # Language Tag.
        'morx',  # Extended Glyph Metamorphosis Table.
        'trak',  # Tracking table.
        'xref',  # The cross-reference table (some Apple font tooling information).
    ]
    # if fontfile is a ttc, specify font number
    options.font_number = fontfile.face_index

    font = subset.load_font(fontfile, options)
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(gids=glyphs)
    subsetter.subset(font)
    return font

