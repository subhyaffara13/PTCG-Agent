
def _get_advance_metrics(font, axisTags, tableFields):
    # There's two ways we can go from here:
    # 1. For each glyph, at each master peak, compute the value of the
    #    advance width at that peak.  Then pass these all to a VariationModel
    #    builder to compute back the deltas.
    # 2. For each master peak, pull out the deltas of the advance width directly,
    #    and feed these to the VarStoreBuilder, forgoing the remodeling step.
    # We'll go with the second option, as it's simpler, faster, and more direct.
    gvar = font["gvar"]
    vhAdvanceDeltasAndSupports = {}
    glyphOrder = font.getGlyphOrder()
    phantomIndex = tableFields.phantomIndex
    for glyphName in glyphOrder:
        supports = []
        deltas = []
        variations = gvar.variations.get(glyphName, [])

        for tv in variations:
            supports.append(tv.axes)
            phantoms = tv.coordinates[-4:]
            phantoms = phantoms[phantomIndex * 2 : phantomIndex * 2 + 2]
            assert len(phantoms) == 2
            phantoms[0] = phantoms[0][phantomIndex] if phantoms[0] is not None else 0
            phantoms[1] = phantoms[1][phantomIndex] if phantoms[1] is not None else 0
            deltas.append(phantoms[1] - phantoms[0])

        vhAdvanceDeltasAndSupports[glyphName] = (deltas, supports)

    vOrigDeltasAndSupports = None  # TODO

    return vhAdvanceDeltasAndSupports, vOrigDeltasAndSupports


def _get_advance_metrics(font, masterModel, master_ttfs, axisTags, tableFields):
    tableTag = tableFields.tableTag
    glyphOrder = font.getGlyphOrder()

    # Build list of source font advance widths for each glyph
    metricsTag = tableFields.metricsTag
    advMetricses = [m[metricsTag].metrics for m in master_ttfs]

    # Build list of source font vertical origin coords for each glyph
    if tableTag == "VVAR" and "VORG" in master_ttfs[0]:
        vOrigMetricses = [m["VORG"].VOriginRecords for m in master_ttfs]
        defaultYOrigs = [m["VORG"].defaultVertOriginY for m in master_ttfs]
        vOrigMetricses = list(zip(vOrigMetricses, defaultYOrigs))
    else:
        vOrigMetricses = None

    vhAdvanceDeltasAndSupports = {}
    vOrigDeltasAndSupports = {}
    # HACK: we treat width 65535 as a sentinel value to signal that a glyph
    # from a non-default master should not participate in computing {H,V}VAR,
    # as if it were missing. Allows to variate other glyph-related data independently
    # from glyph metrics
    sparse_advance = 0xFFFF
    for glyph in glyphOrder:
        vhAdvances = [
            (
                metrics[glyph][0]
                if glyph in metrics and metrics[glyph][0] != sparse_advance
                else None
            )
            for metrics in advMetricses
        ]
        vhAdvanceDeltasAndSupports[glyph] = masterModel.getDeltasAndSupports(
            vhAdvances, round=round
        )

    if vOrigMetricses:
        for glyph in glyphOrder:
            # We need to supply a vOrigs tuple with non-None default values
            # for each glyph. vOrigMetricses contains values only for those
            # glyphs which have a non-default vOrig.
            vOrigs = [
                metrics[glyph] if glyph in metrics else defaultVOrig
                for metrics, defaultVOrig in vOrigMetricses
            ]
            vOrigDeltasAndSupports[glyph] = masterModel.getDeltasAndSupports(
                vOrigs, round=round
            )

    return vhAdvanceDeltasAndSupports, vOrigDeltasAndSupports

