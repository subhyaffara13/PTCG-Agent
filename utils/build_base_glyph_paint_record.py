
def buildBaseGlyphPaintRecord(
    baseGlyph: str, layerBuilder: LayerListBuilder, paint: _PaintInput
) -> ot.BaseGlyphList:
    self = ot.BaseGlyphPaintRecord()
    self.BaseGlyph = baseGlyph
    self.Paint = layerBuilder.buildPaint(paint)
    return self

