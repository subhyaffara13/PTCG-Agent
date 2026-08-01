
def _remove_glyf_overlaps(
    *,
    font: ttFont.TTFont,
    glyphNames: Iterable[str],
    glyphSet: _TTGlyphMapping,
    removeHinting: bool,
    ignoreErrors: bool,
) -> None:
    glyfTable = font["glyf"]
    hmtxTable = font["hmtx"]

    # process all simple glyphs first, then composites with increasing component depth,
    # so that by the time we test for component intersections the respective base glyphs
    # have already been simplified
    glyphNames = sorted(
        glyphNames,
        key=lambda name: (
            (
                glyfTable[name].getCompositeMaxpValues(glyfTable).maxComponentDepth
                if glyfTable[name].isComposite()
                else 0
            ),
            name,
        ),
    )
    modified = set()
    for glyphName in glyphNames:
        try:
            if removeTTGlyphOverlaps(
                glyphName, glyphSet, glyfTable, hmtxTable, removeHinting
            ):
                modified.add(glyphName)
        except RemoveOverlapsError:
            if not ignoreErrors:
                raise
            log.error("Failed to remove overlaps for '%s'", glyphName)

    log.debug("Removed overlaps for %s glyphs:\n%s", len(modified), " ".join(modified))

