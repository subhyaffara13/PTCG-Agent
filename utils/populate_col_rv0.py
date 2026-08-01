
def populateCOLRv0(
    table: ot.COLR,
    colorGlyphsV0: _ColorGlyphsV0Dict,
    glyphMap: Optional[Mapping[str, int]] = None,
):
    """Build v0 color layers and add to existing COLR table.

    Args:
        table: a raw ``otTables.COLR()`` object (not ttLib's ``table_C_O_L_R_``).
        colorGlyphsV0: map of base glyph names to lists of (layer glyph names,
            color palette index) tuples. Can be empty.
        glyphMap: a map from glyph names to glyph indices, as returned from
            ``TTFont.getReverseGlyphMap()``, to optionally sort base records by GID.
    """
    if glyphMap is not None:
        _check_base_glyphs_exist(colorGlyphsV0, glyphMap, "populateCOLRv0")
        colorGlyphItems = sorted(
            colorGlyphsV0.items(), key=lambda item: glyphMap[item[0]]
        )
    else:
        colorGlyphItems = colorGlyphsV0.items()
    baseGlyphRecords = []
    layerRecords = []
    for baseGlyph, layers in colorGlyphItems:
        baseRec = ot.BaseGlyphRecord()
        baseRec.BaseGlyph = baseGlyph
        baseRec.FirstLayerIndex = len(layerRecords)
        baseRec.NumLayers = len(layers)
        baseGlyphRecords.append(baseRec)

        for layerGlyph, paletteIndex in layers:
            layerRec = ot.LayerRecord()
            layerRec.LayerGlyph = layerGlyph
            layerRec.PaletteIndex = paletteIndex
            layerRecords.append(layerRec)

    table.BaseGlyphRecordArray = table.LayerRecordArray = None
    if baseGlyphRecords:
        table.BaseGlyphRecordArray = ot.BaseGlyphRecordArray()
        table.BaseGlyphRecordArray.BaseGlyphRecord = baseGlyphRecords
    if layerRecords:
        table.LayerRecordArray = ot.LayerRecordArray()
        table.LayerRecordArray.LayerRecord = layerRecords
    table.BaseGlyphRecordCount = len(baseGlyphRecords)
    table.LayerRecordCount = len(layerRecords)

