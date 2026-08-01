
def _instantiateVHVAR(varfont, axisLimits, tableFields, *, round=round):
    location = axisLimits.pinnedLocation()
    tableTag = tableFields.tableTag
    fvarAxes = varfont["fvar"].axes

    log.info("Instantiating %s table", tableTag)
    vhvar = varfont[tableTag].table
    varStore = vhvar.VarStore

    if "glyf" in varfont:
        # Deltas from gvar table have already been applied to the hmtx/vmtx. For full
        # instances (i.e. all axes pinned), we can simply drop HVAR/VVAR and return
        if set(location).issuperset(axis.axisTag for axis in fvarAxes):
            log.info("Dropping %s table", tableTag)
            del varfont[tableTag]
            return

    defaultDeltas = instantiateItemVariationStore(varStore, fvarAxes, axisLimits)

    if "glyf" not in varfont:
        # CFF2 fonts need hmtx/vmtx updated here. For glyf fonts, the instantiateGvar
        # function already updated the hmtx/vmtx from phantom points. Maybe remove
        # that and do it here for both CFF2 and glyf fonts?
        #
        # Specially, if a font has glyf but not gvar, the hmtx/vmtx will not have been
        # updated by instantiateGvar. Though one can call that a faulty font.
        metricsTag = "vmtx" if tableTag == "VVAR" else "hmtx"
        if metricsTag in varfont:
            advMapping = getattr(vhvar, tableFields.advMapping)
            metricsTable = varfont[metricsTag]
            metrics = metricsTable.metrics
            for glyphName, (advanceWidth, sb) in metrics.items():
                if advMapping:
                    varIdx = advMapping.mapping[glyphName]
                else:
                    varIdx = varfont.getGlyphID(glyphName)
                delta = round(defaultDeltas[varIdx])
                metrics[glyphName] = (max(0, advanceWidth + delta), sb)

            if (
                tableTag == "VVAR"
                and getattr(vhvar, tableFields.vOrigMapping) is not None
            ):
                log.warning(
                    "VORG table not yet updated to reflect changes in VVAR table"
                )

            # For full instances (i.e. all axes pinned), we can simply drop HVAR/VVAR and return
            if set(location).issuperset(axis.axisTag for axis in fvarAxes):
                log.info("Dropping %s table", tableTag)
                del varfont[tableTag]
                return

    if varStore.VarRegionList.Region:
        # Only re-optimize VarStore if the HVAR/VVAR already uses indirect AdvWidthMap
        # or AdvHeightMap. If a direct, implicit glyphID->VariationIndex mapping is
        # used for advances, skip re-optimizing and maintain original VariationIndex.
        if getattr(vhvar, tableFields.advMapping):
            varIndexMapping = varStore.optimize(use_NO_VARIATION_INDEX=False)
            glyphOrder = varfont.getGlyphOrder()
            _remapVarIdxMap(vhvar, tableFields.advMapping, varIndexMapping, glyphOrder)
            if getattr(vhvar, tableFields.sb1):  # left or top sidebearings
                _remapVarIdxMap(vhvar, tableFields.sb1, varIndexMapping, glyphOrder)
            if getattr(vhvar, tableFields.sb2):  # right or bottom sidebearings
                _remapVarIdxMap(vhvar, tableFields.sb2, varIndexMapping, glyphOrder)
            if tableTag == "VVAR" and getattr(vhvar, tableFields.vOrigMapping):
                _remapVarIdxMap(
                    vhvar, tableFields.vOrigMapping, varIndexMapping, glyphOrder
                )

