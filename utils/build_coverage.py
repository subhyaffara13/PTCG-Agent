
def buildCoverage(glyphs, glyphMap):
    """Builds a coverage table.

    Coverage tables (as defined in the `OpenType spec <https://docs.microsoft.com/en-gb/typography/opentype/spec/chapter2#coverage-table>`__)
    are used in all OpenType Layout lookups apart from the Extension type, and
    define the glyphs involved in a layout subtable. This allows shaping engines
    to compare the glyph stream with the coverage table and quickly determine
    whether a subtable should be involved in a shaping operation.

    This function takes a list of glyphs and a glyphname-to-ID map, and
    returns a ``Coverage`` object representing the coverage table.

    Example::

        glyphMap = font.getReverseGlyphMap()
        glyphs = [ "A", "B", "C" ]
        coverage = buildCoverage(glyphs, glyphMap)

    Args:
        glyphs: a sequence of glyph names.
        glyphMap: a glyph name to ID map, typically returned from
            ``font.getReverseGlyphMap()``.

    Returns:
        An ``otTables.Coverage`` object (empty if no glyphs supplied).
    """
    # Per the OpenType spec: "For cases in which subtable offset fields are not
    # documented as permitting NULL values, font compilers must include a subtable
    # of the indicated format, even if it is a header stub without further data
    # (for example, a coverage table with no glyph IDs)."
    # https://github.com/fonttools/fonttools/issues/4003
    self = ot.Coverage()
    if glyphs:
        try:
            self.glyphs = sorted(set(glyphs), key=glyphMap.__getitem__)
        except KeyError as e:
            raise ValueError(f"Could not find glyph {e} in font") from e
    else:
        self.glyphs = []
    return self

