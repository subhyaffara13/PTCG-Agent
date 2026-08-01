
def _remove_cff_overlaps(
    *,
    font: ttFont.TTFont,
    glyphNames: Iterable[str],
    glyphSet: _TTGlyphMapping,
    removeHinting: bool,
    ignoreErrors: bool,
    table_tag: str,
    removeUnusedSubroutines: bool = True,
) -> None:
    cffFontSet = font[table_tag].cff
    modified = set()
    for glyphName in glyphNames:
        try:
            if _remove_charstring_overlaps(
                glyphName=glyphName,
                glyphSet=glyphSet,
                cffFontSet=cffFontSet,
            ):
                modified.add(glyphName)
        except RemoveOverlapsError:
            if not ignoreErrors:
                raise
            log.error("Failed to remove overlaps for '%s'", glyphName)

    if not modified:
        log.debug("No overlaps found in the specified CFF glyphs")
        return

    if removeHinting:
        cffFontSet.remove_hints()

    if removeUnusedSubroutines:
        cffFontSet.remove_unused_subroutines()

    log.debug("Removed overlaps for %s glyphs:\n%s", len(modified), " ".join(modified))

