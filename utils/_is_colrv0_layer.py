
def _is_colrv0_layer(layer: Any) -> bool:
    # Consider as COLRv0 layer any sequence of length 2 (be it tuple or list) in which
    # the first element is a str (the layerGlyph) and the second element is an int
    # (CPAL paletteIndex).
    # https://github.com/googlefonts/ufo2ft/issues/426
    try:
        layerGlyph, paletteIndex = layer
    except (TypeError, ValueError):
        return False
    else:
        return isinstance(layerGlyph, str) and isinstance(paletteIndex, int)

