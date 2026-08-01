
def removeOverlaps(
    font: ttFont.TTFont,
    glyphNames: Optional[Iterable[str]] = None,
    removeHinting: bool = True,
    ignoreErrors: bool = False,
    *,
    removeUnusedSubroutines: bool = True,
) -> None:
    """Simplify glyphs in TTFont by merging overlapping contours.

    Overlapping components are first decomposed to simple contours, then merged.

    Currently this only works for fonts with 'glyf' or 'CFF ' tables.
    Raises NotImplementedError if 'glyf' or 'CFF ' tables are absent.

    Note that removing overlaps invalidates the hinting. By default we drop hinting
    from all glyphs whether or not overlaps are removed from a given one, as it would
    look weird if only some glyphs are left (un)hinted.

    Args:
        font: input TTFont object, modified in place.
        glyphNames: optional iterable of glyph names (str) to remove overlaps from.
            By default, all glyphs in the font are processed.
        removeHinting (bool): set to False to keep hinting for unmodified glyphs.
        ignoreErrors (bool): set to True to ignore errors while removing overlaps,
            thus keeping the tricky glyphs unchanged (fonttools/fonttools#2363).
        removeUnusedSubroutines (bool): set to False to keep unused subroutines
            in CFF table after removing overlaps. Default is to remove them if
            any glyphs are modified.
    """

    if "glyf" not in font and "CFF " not in font and "CFF2" not in font:
        raise NotImplementedError(
            "No outline data found in the font: missing 'glyf', 'CFF ', or 'CFF2' table"
        )

    if glyphNames is None:
        glyphNames = font.getGlyphOrder()

    # Wraps the underlying glyphs, takes care of interfacing with drawing pens
    glyphSet = font.getGlyphSet()

    if "glyf" in font:
        _remove_glyf_overlaps(
            font=font,
            glyphNames=glyphNames,
            glyphSet=glyphSet,
            removeHinting=removeHinting,
            ignoreErrors=ignoreErrors,
        )

    if "CFF " in font or "CFF2" in font:
        _remove_cff_overlaps(
            font=font,
            glyphNames=glyphNames,
            glyphSet=glyphSet,
            removeHinting=removeHinting,
            ignoreErrors=ignoreErrors,
            table_tag="CFF " if "CFF " in font else "CFF2",
            removeUnusedSubroutines=removeUnusedSubroutines,
        )

