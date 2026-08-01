
def instantiateGvar(varfont, axisLimits, optimize=True):
    log.info("Instantiating glyf/gvar tables")

    gvar = varfont["gvar"]
    glyf = varfont["glyf"]
    hMetrics = varfont["hmtx"].metrics
    vMetrics = getattr(varfont.get("vmtx"), "metrics", None)
    # Get list of glyph names sorted by component depth.
    # If a composite glyph is processed before its base glyph, the bounds may
    # be calculated incorrectly because deltas haven't been applied to the
    # base glyph yet.
    glyphnames = sorted(
        glyf.glyphOrder,
        key=lambda name: (
            (
                glyf[name].getCompositeMaxpValues(glyf).maxComponentDepth
                if glyf[name].isComposite()
                else 0
            ),
            name,
        ),
    )
    for glyphname in glyphnames:
        _instantiateGvarGlyph(
            glyphname, glyf, gvar, hMetrics, vMetrics, axisLimits, optimize=optimize
        )

    if not gvar.variations:
        del varfont["gvar"]

