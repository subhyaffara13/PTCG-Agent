
def _getGlyphsFromCoverageTable(coverage):
    if coverage is None:
        # empty coverage table
        return []
    else:
        return coverage.glyphs

