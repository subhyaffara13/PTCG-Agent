
def _add_gvar(font, masterModel, master_ttfs, tolerance=0.5, optimize=True):
    if tolerance < 0:
        raise ValueError("`tolerance` must be a positive number.")

    log.info("Generating gvar")
    assert "gvar" not in font
    gvar = font["gvar"] = newTable("gvar")
    glyf = font["glyf"]
    defaultMasterIndex = masterModel.reverseMapping[0]

    master_datas = [
        _MasterData(
            m["glyf"], m["hmtx"].metrics, getattr(m.get("vmtx"), "metrics", None)
        )
        for m in master_ttfs
    ]

    for glyph in font.getGlyphOrder():
        log.debug("building gvar for glyph '%s'", glyph)

        allData = [
            m.glyf._getCoordinatesAndControls(glyph, m.hMetrics, m.vMetrics)
            for m in master_datas
        ]

        if allData[defaultMasterIndex][1].numberOfContours != 0:
            # If the default master is not empty, interpret empty non-default masters
            # as missing glyphs from a sparse master
            allData = [
                d if d is not None and d[1].numberOfContours != 0 else None
                for d in allData
            ]

        model, allData = masterModel.getSubModel(allData)

        allCoords = [d[0] for d in allData]
        allControls = [d[1] for d in allData]
        control = allControls[0]
        if not models.allEqual(allControls):
            log.warning("glyph %s has incompatible masters; skipping" % glyph)
            continue
        del allControls

        # Update gvar
        gvar.variations[glyph] = []
        deltas = model.getDeltas(
            allCoords, round=partial(GlyphCoordinates.__round__, round=round)
        )
        supports = model.supports
        assert len(deltas) == len(supports)

        # Prepare for IUP optimization
        origCoords = deltas[0]
        endPts = control.endPts

        for i, (delta, support) in enumerate(zip(deltas[1:], supports[1:])):
            if all(v == 0 for v in delta.array):
                continue
            var = TupleVariation(support, delta)
            if optimize:
                var.optimize(origCoords, endPts, tolerance=tolerance)
            gvar.variations[glyph].append(var)

