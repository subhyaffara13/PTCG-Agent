
def _add_VHVAR(font, axisTags, tableFields, getAdvanceMetrics):
    tableTag = tableFields.tableTag
    assert tableTag not in font
    glyphOrder = font.getGlyphOrder()
    log.info("Generating " + tableTag)
    VHVAR = newTable(tableTag)
    tableClass = getattr(ot, tableTag)
    vhvar = VHVAR.table = tableClass()
    vhvar.Version = 0x00010000

    vhAdvanceDeltasAndSupports, vOrigDeltasAndSupports = getAdvanceMetrics()

    if vOrigDeltasAndSupports:
        singleModel = False
    else:
        singleModel = models.allEqual(
            id(v[1]) for v in vhAdvanceDeltasAndSupports.values()
        )

    directStore = None
    if singleModel:
        # Build direct mapping
        supports = next(iter(vhAdvanceDeltasAndSupports.values()))[1][1:]
        varTupleList = builder.buildVarRegionList(supports, axisTags)
        varTupleIndexes = list(range(len(supports)))
        varData = builder.buildVarData(varTupleIndexes, [], optimize=False)
        for glyphName in glyphOrder:
            varData.addItem(vhAdvanceDeltasAndSupports[glyphName][0], round=noRound)
        varData.optimize()
        directStore = builder.buildVarStore(varTupleList, [varData])
        # remove unused regions from VarRegionList
        directStore.prune_regions()

    # Build optimized indirect mapping
    storeBuilder = varStore.OnlineVarStoreBuilder(axisTags)
    advMapping = {}
    for glyphName in glyphOrder:
        deltas, supports = vhAdvanceDeltasAndSupports[glyphName]
        storeBuilder.setSupports(supports)
        advMapping[glyphName] = storeBuilder.storeDeltas(deltas, round=noRound)

    if vOrigDeltasAndSupports:
        vOrigMap = {}
        for glyphName in glyphOrder:
            deltas, supports = vOrigDeltasAndSupports[glyphName]
            storeBuilder.setSupports(supports)
            vOrigMap[glyphName] = storeBuilder.storeDeltas(deltas, round=noRound)

    indirectStore = storeBuilder.finish()
    mapping2 = indirectStore.optimize(use_NO_VARIATION_INDEX=False)
    advMapping = [mapping2[advMapping[g]] for g in glyphOrder]
    advanceMapping = builder.buildVarIdxMap(advMapping, glyphOrder)

    if vOrigDeltasAndSupports:
        vOrigMap = [mapping2[vOrigMap[g]] for g in glyphOrder]

    useDirect = False
    vOrigMapping = None
    if directStore:
        # Compile both, see which is more compact

        writer = OTTableWriter()
        directStore.compile(writer, font)
        directSize = len(writer.getAllData())

        writer = OTTableWriter()
        indirectStore.compile(writer, font)
        advanceMapping.compile(writer, font)
        indirectSize = len(writer.getAllData())

        useDirect = directSize < indirectSize

    if useDirect:
        metricsStore = directStore
        advanceMapping = None
    else:
        metricsStore = indirectStore
        if vOrigDeltasAndSupports:
            vOrigMapping = builder.buildVarIdxMap(vOrigMap, glyphOrder)

    vhvar.VarStore = metricsStore
    setattr(vhvar, tableFields.advMapping, advanceMapping)
    if vOrigMapping is not None:
        setattr(vhvar, tableFields.vOrigMapping, vOrigMapping)
    setattr(vhvar, tableFields.sb1, None)
    setattr(vhvar, tableFields.sb2, None)

    font[tableTag] = VHVAR
    return

