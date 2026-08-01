
def instantiateGvarGlyph(varfont, glyphname, axisLimits, optimize=True):
    """Remove?
    https://github.com/fonttools/fonttools/pull/2266"""
    gvar = varfont["gvar"]
    glyf = varfont["glyf"]
    hMetrics = varfont["hmtx"].metrics
    vMetrics = getattr(varfont.get("vmtx"), "metrics", None)
    _instantiateGvarGlyph(
        glyphname, glyf, gvar, hMetrics, vMetrics, axisLimits, optimize=optimize
    )

