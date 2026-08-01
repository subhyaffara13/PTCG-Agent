
def computeMegaCmap(merger, cmapTables):
    """Sets merger.cmap and merger.uvsDict."""

    # TODO Handle format=14.
    # Only merge format 4 and 12 Unicode subtables, ignores all other subtables
    # If there is a format 12 table for a font, ignore the format 4 table of it
    chosenCmapTables = []
    chosenUvsTables = []
    for fontIdx, table in enumerate(cmapTables):
        format4 = None
        format12 = None
        format14 = None
        for subtable in table.tables:
            properties = (subtable.format, subtable.platformID, subtable.platEncID)
            if properties in _CmapUnicodePlatEncodings.BMP:
                format4 = subtable
            elif properties in _CmapUnicodePlatEncodings.FullRepertoire:
                format12 = subtable
            elif properties in _CmapUnicodePlatEncodings.UVS:
                format14 = subtable
            else:
                log.warning(
                    "Dropped cmap subtable from font '%s':\t"
                    "format %2s, platformID %2s, platEncID %2s",
                    fontIdx,
                    subtable.format,
                    subtable.platformID,
                    subtable.platEncID,
                )
        if format12 is not None:
            chosenCmapTables.append((format12, fontIdx))
        elif format4 is not None:
            chosenCmapTables.append((format4, fontIdx))

        if format14 is not None:
            chosenUvsTables.append(format14)

    # Build the unicode mapping
    merger.cmap = cmap = {}
    fontIndexForGlyph = {}
    glyphSets = [None for f in merger.fonts] if hasattr(merger, "fonts") else None

    for table, fontIdx in chosenCmapTables:
        # handle duplicates
        for uni, gid in table.cmap.items():
            oldgid = cmap.get(uni, None)
            if oldgid is None:
                cmap[uni] = gid
                fontIndexForGlyph[gid] = fontIdx
            elif is_Default_Ignorable(uni) or uni in (0x25CC,):  # U+25CC DOTTED CIRCLE
                continue
            elif oldgid != gid:
                # Char previously mapped to oldgid, now to gid.
                # Record, to fix up in GSUB 'locl' later.
                if merger.duplicateGlyphsPerFont[fontIdx].get(oldgid) is None:
                    if glyphSets is not None:
                        oldFontIdx = fontIndexForGlyph[oldgid]
                        for idx in (fontIdx, oldFontIdx):
                            if glyphSets[idx] is None:
                                glyphSets[idx] = merger.fonts[idx].getGlyphSet()
                        # if _glyphsAreSame(glyphSets[oldFontIdx], glyphSets[fontIdx], oldgid, gid):
                        # 	continue
                    merger.duplicateGlyphsPerFont[fontIdx][oldgid] = gid
                elif merger.duplicateGlyphsPerFont[fontIdx][oldgid] != gid:
                    # Char previously mapped to oldgid but oldgid is already remapped to a different
                    # gid, because of another Unicode character.
                    # TODO: Try harder to do something about these.
                    log.warning(
                        "Dropped mapping from codepoint %#06X to glyphId '%s'", uni, gid
                    )

    merger.uvsDict = computeMegaUvs(merger, chosenUvsTables)

