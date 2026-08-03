from typing import Optional, Tuple

def buildColrV1(
    colorGlyphs: _ColorGlyphsDict,
    glyphMap: Optional[Mapping[str, int]] = None,
    *,
    allowLayerReuse: bool = True,
) -> Tuple[Optional[ot.LayerList], ot.BaseGlyphList]:
    if glyphMap is not None:
        _check_base_glyphs_exist(colorGlyphs, glyphMap, "buildColrV1")
        colorGlyphItems = sorted(
            colorGlyphs.items(), key=lambda item: glyphMap[item[0]]
        )
    else:
        colorGlyphItems = colorGlyphs.items()

    errors = {}
    baseGlyphs = []
    layerBuilder = LayerListBuilder(allowLayerReuse=allowLayerReuse)
    for baseGlyph, paint in colorGlyphItems:
        try:
            baseGlyphs.append(buildBaseGlyphPaintRecord(baseGlyph, layerBuilder, paint))

        except (ColorLibError, OverflowError, ValueError, TypeError) as e:
            errors[baseGlyph] = e

    if errors:
        failed_glyphs = _format_glyph_errors(errors)
        exc = ColorLibError(f"Failed to build BaseGlyphList:\n{failed_glyphs}")
        exc.errors = errors
        raise exc from next(iter(errors.values()))

    layers = layerBuilder.build()
    glyphs = ot.BaseGlyphList()
    glyphs.BaseGlyphCount = len(baseGlyphs)
    glyphs.BaseGlyphPaintRecord = baseGlyphs
    return (layers, glyphs)

