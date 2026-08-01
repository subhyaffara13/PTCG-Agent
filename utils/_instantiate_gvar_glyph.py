
def _instantiateGvarGlyph(
    glyphname, glyf, gvar, hMetrics, vMetrics, axisLimits, optimize=True
):
    coordinates, ctrl = glyf._getCoordinatesAndControls(glyphname, hMetrics, vMetrics)
    endPts = ctrl.endPts

    # Not every glyph may have variations
    tupleVarStore = gvar.variations.get(glyphname)

    if tupleVarStore:
        defaultDeltas = instantiateTupleVariationStore(
            tupleVarStore, axisLimits, coordinates, endPts
        )

        if defaultDeltas:
            coordinates += _g_l_y_f.GlyphCoordinates(defaultDeltas)

    # _setCoordinates also sets the hmtx/vmtx advance widths and sidebearings from
    # the four phantom points and glyph bounding boxes.
    # We call it unconditionally even if a glyph has no variations or no deltas are
    # applied at this location, in case the glyph's xMin and in turn its sidebearing
    # have changed. E.g. a composite glyph has no deltas for the component's (x, y)
    # offset nor for the 4 phantom points (e.g. it's monospaced). Thus its entry in
    # gvar table is empty; however, the composite's base glyph may have deltas
    # applied, hence the composite's bbox and left/top sidebearings may need updating
    # in the instanced font.
    glyf._setCoordinates(glyphname, coordinates, hMetrics, vMetrics)

    if not tupleVarStore:
        if glyphname in gvar.variations:
            del gvar.variations[glyphname]
        return

    if optimize:
        # IUP semantics depend on point equality, and so round prior to
        # optimization to ensure that comparisons that happen now will be the
        # same as those that happen at render time. This is especially needed
        # when floating point deltas have been applied to the default position.
        #     See https://github.com/fonttools/fonttools/issues/3634
        # Rounding must happen only after calculating glyf metrics above, to
        # preserve backwards compatibility.
        #     See 0010a3cd9aa25f84a3a6250dafb119743d32aa40
        coordinates.toInt()
        for var in tupleVarStore:
            var.optimize(coordinates, endPts)

