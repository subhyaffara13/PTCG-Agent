
def instantiateVariableFont(varfont, location, inplace=False, overlap=True):
    """Generate a static instance from a variable TTFont and a dictionary
    defining the desired location along the variable font's axes.
    The location values must be specified as user-space coordinates, e.g.:

    .. code-block::

        {'wght': 400, 'wdth': 100}

    By default, a new TTFont object is returned. If ``inplace`` is True, the
    input varfont is modified and reduced to a static font.

    When the overlap parameter is defined as True,
    OVERLAP_SIMPLE and OVERLAP_COMPOUND bits are set to 1.  See
    https://docs.microsoft.com/en-us/typography/opentype/spec/glyf
    """
    if not inplace:
        # make a copy to leave input varfont unmodified
        stream = BytesIO()
        varfont.save(stream)
        stream.seek(0)
        varfont = TTFont(stream)

    fvar = varfont["fvar"]
    axes = {a.axisTag: (a.minValue, a.defaultValue, a.maxValue) for a in fvar.axes}
    loc = normalizeLocation(location, axes)
    if "avar" in varfont:
        maps = varfont["avar"].segments
        loc = {k: piecewiseLinearMap(v, maps[k]) for k, v in loc.items()}
    # Quantize to F2Dot14, to avoid surprise interpolations.
    loc = {k: floatToFixedToFloat(v, 14) for k, v in loc.items()}
    # Location is normalized now
    log.info("Normalized location: %s", loc)

    if "gvar" in varfont:
        log.info("Mutating glyf/gvar tables")
        gvar = varfont["gvar"]
        glyf = varfont["glyf"]
        hMetrics = varfont["hmtx"].metrics
        vMetrics = getattr(varfont.get("vmtx"), "metrics", None)
        # get list of glyph names in gvar sorted by component depth
        glyphnames = sorted(
            gvar.variations.keys(),
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
            variations = gvar.variations[glyphname]
            coordinates, _ = glyf._getCoordinatesAndControls(
                glyphname, hMetrics, vMetrics
            )
            origCoords, endPts = None, None
            for var in variations:
                scalar = supportScalar(loc, var.axes)
                if not scalar:
                    continue
                delta = var.coordinates
                if None in delta:
                    if origCoords is None:
                        origCoords, g = glyf._getCoordinatesAndControls(
                            glyphname, hMetrics, vMetrics
                        )
                    delta = iup_delta(delta, origCoords, g.endPts)
                coordinates += GlyphCoordinates(delta) * scalar
            glyf._setCoordinates(glyphname, coordinates, hMetrics, vMetrics)
    else:
        glyf = None

    if "DSIG" in varfont:
        del varfont["DSIG"]

    if "cvar" in varfont:
        log.info("Mutating cvt/cvar tables")
        cvar = varfont["cvar"]
        cvt = varfont["cvt "]
        deltas = {}
        for var in cvar.variations:
            scalar = supportScalar(loc, var.axes)
            if not scalar:
                continue
            for i, c in enumerate(var.coordinates):
                if c is not None:
                    deltas[i] = deltas.get(i, 0) + scalar * c
        for i, delta in deltas.items():
            cvt[i] += otRound(delta)

    if "CFF2" in varfont:
        log.info("Mutating CFF2 table")
        glyphOrder = varfont.getGlyphOrder()
        CFF2 = varfont["CFF2"]
        topDict = CFF2.cff.topDictIndex[0]
        vsInstancer = VarStoreInstancer(topDict.VarStore.otVarStore, fvar.axes, loc)
        interpolateFromDeltas = vsInstancer.interpolateFromDeltas
        interpolate_cff2_PrivateDict(topDict, interpolateFromDeltas)
        CFF2.desubroutinize()
        interpolate_cff2_charstrings(topDict, interpolateFromDeltas, glyphOrder)
        interpolate_cff2_metrics(varfont, topDict, glyphOrder, loc)
        del topDict.rawDict["VarStore"]
        del topDict.VarStore

    if "MVAR" in varfont:
        log.info("Mutating MVAR table")
        mvar = varfont["MVAR"].table
        varStoreInstancer = VarStoreInstancer(mvar.VarStore, fvar.axes, loc)
        records = mvar.ValueRecord
        for rec in records:
            mvarTag = rec.ValueTag
            if mvarTag not in MVAR_ENTRIES:
                continue
            tableTag, itemName = MVAR_ENTRIES[mvarTag]
            delta = otRound(varStoreInstancer[rec.VarIdx])
            if not delta:
                continue
            setattr(
                varfont[tableTag],
                itemName,
                getattr(varfont[tableTag], itemName) + delta,
            )

    log.info("Mutating FeatureVariations")
    for tableTag in "GSUB", "GPOS":
        if not tableTag in varfont:
            continue
        table = varfont[tableTag].table
        if not getattr(table, "FeatureVariations", None):
            continue
        variations = table.FeatureVariations
        for record in variations.FeatureVariationRecord:
            applies = True
            for condition in record.ConditionSet.ConditionTable:
                if condition.Format == 1:
                    axisIdx = condition.AxisIndex
                    axisTag = fvar.axes[axisIdx].axisTag
                    Min = condition.FilterRangeMinValue
                    Max = condition.FilterRangeMaxValue
                    v = loc[axisTag]
                    if not (Min <= v <= Max):
                        applies = False
                else:
                    applies = False
                if not applies:
                    break

            if applies:
                assert record.FeatureTableSubstitution.Version == 0x00010000
                for rec in record.FeatureTableSubstitution.SubstitutionRecord:
                    table.FeatureList.FeatureRecord[rec.FeatureIndex].Feature = (
                        rec.Feature
                    )
                break
        del table.FeatureVariations

    if "GDEF" in varfont and varfont["GDEF"].table.Version >= 0x00010003:
        log.info("Mutating GDEF/GPOS/GSUB tables")
        gdef = varfont["GDEF"].table
        instancer = VarStoreInstancer(gdef.VarStore, fvar.axes, loc)

        merger = MutatorMerger(varfont, instancer)
        merger.mergeTables(varfont, [varfont], ["GDEF", "GPOS"])

        # Downgrade GDEF.
        del gdef.VarStore
        gdef.Version = 0x00010002
        if gdef.MarkGlyphSetsDef is None:
            del gdef.MarkGlyphSetsDef
            gdef.Version = 0x00010000

        if not (
            gdef.LigCaretList
            or gdef.MarkAttachClassDef
            or gdef.GlyphClassDef
            or gdef.AttachList
            or (gdef.Version >= 0x00010002 and gdef.MarkGlyphSetsDef)
        ):
            del varfont["GDEF"]

    addidef = False
    if glyf:
        for glyph in glyf.glyphs.values():
            if hasattr(glyph, "program"):
                instructions = glyph.program.getAssembly()
                # If GETVARIATION opcode is used in bytecode of any glyph add IDEF
                addidef = any(op.startswith("GETVARIATION") for op in instructions)
                if addidef:
                    break
        if overlap:
            for glyph_name in glyf.keys():
                glyph = glyf[glyph_name]
                # Set OVERLAP_COMPOUND bit for compound glyphs
                if glyph.isComposite():
                    glyph.components[0].flags |= OVERLAP_COMPOUND
                # Set OVERLAP_SIMPLE bit for simple glyphs
                elif glyph.numberOfContours > 0:
                    glyph.flags[0] |= flagOverlapSimple
    if addidef:
        log.info("Adding IDEF to fpgm table for GETVARIATION opcode")
        asm = []
        if "fpgm" in varfont:
            fpgm = varfont["fpgm"]
            asm = fpgm.program.getAssembly()
        else:
            fpgm = newTable("fpgm")
            fpgm.program = ttProgram.Program()
            varfont["fpgm"] = fpgm
        asm.append("PUSHB[000] 145")
        asm.append("IDEF[ ]")
        args = [str(len(loc))]
        for a in fvar.axes:
            args.append(str(floatToFixed(loc[a.axisTag], 14)))
        asm.append("NPUSHW[ ] " + " ".join(args))
        asm.append("ENDF[ ]")
        fpgm.program.fromAssembly(asm)

        # Change maxp attributes as IDEF is added
        if "maxp" in varfont:
            maxp = varfont["maxp"]
            setattr(
                maxp, "maxInstructionDefs", 1 + getattr(maxp, "maxInstructionDefs", 0)
            )
            setattr(
                maxp,
                "maxStackElements",
                max(len(loc), getattr(maxp, "maxStackElements", 0)),
            )

    if "name" in varfont:
        log.info("Pruning name table")
        exclude = {a.axisNameID for a in fvar.axes}
        for i in fvar.instances:
            exclude.add(i.subfamilyNameID)
            exclude.add(i.postscriptNameID)
        if "ltag" in varfont:
            # Drop the whole 'ltag' table if all its language tags are referenced by
            # name records to be pruned.
            # TODO: prune unused ltag tags and re-enumerate langIDs accordingly
            excludedUnicodeLangIDs = [
                n.langID
                for n in varfont["name"].names
                if n.nameID in exclude and n.platformID == 0 and n.langID != 0xFFFF
            ]
            if set(excludedUnicodeLangIDs) == set(range(len((varfont["ltag"].tags)))):
                del varfont["ltag"]
        varfont["name"].names[:] = [
            n
            for n in varfont["name"].names
            if n.nameID < 256 or n.nameID not in exclude
        ]

    if "wght" in location and "OS/2" in varfont:
        varfont["OS/2"].usWeightClass = otRound(max(1, min(location["wght"], 1000)))
    if "wdth" in location:
        wdth = location["wdth"]
        for percent, widthClass in sorted(OS2_WIDTH_CLASS_VALUES.items()):
            if wdth < percent:
                varfont["OS/2"].usWidthClass = widthClass
                break
        else:
            varfont["OS/2"].usWidthClass = 9
    if "slnt" in location and "post" in varfont:
        varfont["post"].italicAngle = max(-90, min(location["slnt"], 90))

    log.info("Removing variable tables")
    for tag in ("avar", "cvar", "fvar", "gvar", "HVAR", "MVAR", "VVAR", "STAT"):
        if tag in varfont:
            del varfont[tag]

    return varfont


def instantiateVariableFont(
    varfont,
    axisLimits,
    inplace=False,
    optimize=True,
    overlap=OverlapMode.KEEP_AND_SET_FLAGS,
    updateFontNames=False,
    *,
    downgradeCFF2=False,
    static=False,
):
    """Instantiate variable font, either fully or partially.

    Depending on whether the `axisLimits` dictionary references all or some of the
    input varfont's axes, the output font will either be a full instance (static
    font) or a variable font with possibly less variation data.

    Args:
        varfont: a TTFont instance, which must contain at least an 'fvar' table.
        axisLimits: a dict keyed by axis tags (str) containing the coordinates (float)
            along one or more axes where the desired instance will be located.
            If the value is `None`, the default coordinate as per 'fvar' table for
            that axis is used.
            The limit values can also be (min, max) tuples for restricting an
            axis's variation range. The default axis value must be included in
            the new range.
        inplace (bool): whether to modify input TTFont object in-place instead of
            returning a distinct object.
        optimize (bool): if False, do not perform IUP-delta optimization on the
            remaining 'gvar' table's deltas. Possibly faster, and might work around
            rendering issues in some buggy environments, at the cost of a slightly
            larger file size.
        overlap (OverlapMode): variable fonts usually contain overlapping contours, and
            some font rendering engines on Apple platforms require that the
            `OVERLAP_SIMPLE` and `OVERLAP_COMPOUND` flags in the 'glyf' table be set to
            force rendering using a non-zero fill rule. Thus we always set these flags
            on all glyphs to maximise cross-compatibility of the generated instance.
            You can disable this by passing OverlapMode.KEEP_AND_DONT_SET_FLAGS.
            If you want to remove the overlaps altogether and merge overlapping
            contours and components, you can pass OverlapMode.REMOVE (or
            REMOVE_AND_IGNORE_ERRORS to not hard-fail on tricky glyphs). Note that this
            requires the skia-pathops package (available to pip install).
            The overlap parameter only has effect when generating full static instances.
        updateFontNames (bool): if True, update the instantiated font's name table using
            the Axis Value Tables from the STAT table. The name table and the style bits
            in the head and OS/2 table will be updated so they conform to the R/I/B/BI
            model. If the STAT table is missing or an Axis Value table is missing for
            a given axis coordinate, a ValueError will be raised.
        downgradeCFF2 (bool): if True, downgrade the CFF2 table to CFF table when possible
            ie. full instancing of all axes. This is useful for compatibility with older
            software that does not support CFF2. Defaults to False. Note that this
            operation also removes overlaps within glyph shapes, as CFF does not support
            overlaps but CFF2 does.
        static (bool): if True, generate a full instance (static font) instead of a partial
            instance (variable font).
    """
    # 'overlap' used to be bool and is now enum; for backward compat keep accepting bool
    overlap = OverlapMode(int(overlap))

    sanityCheckVariableTables(varfont)

    if static:
        unspecified = []
        for axis in varfont["fvar"].axes:
            if axis.axisTag not in axisLimits:
                axisLimits[axis.axisTag] = None
                unspecified.append(axis.axisTag)
        if unspecified:
            log.info("Pinning unspecified axes to default: %s", unspecified)

    axisLimits = AxisLimits(axisLimits).limitAxesAndPopulateDefaults(varfont)

    log.info("Restricted limits: %s", axisLimits)

    normalizedLimits = axisLimits.normalize(varfont)

    log.info("Normalized limits: %s", normalizedLimits)

    if not inplace:
        varfont = deepcopy(varfont)

    if "DSIG" in varfont:
        del varfont["DSIG"]

    if updateFontNames:
        log.info("Updating name table")
        names.updateNameTable(varfont, axisLimits)

    if "VARC" in varfont:
        instantiateVARC(varfont, normalizedLimits)

    if "CFF2" in varfont:
        downgradeCFF2 = instantiateCFF2(
            varfont, normalizedLimits, downgrade=downgradeCFF2
        )

    if "gvar" in varfont:
        instantiateGvar(varfont, normalizedLimits, optimize=optimize)

    if "cvar" in varfont:
        instantiateCvar(varfont, normalizedLimits)

    if "MVAR" in varfont:
        instantiateMVAR(varfont, normalizedLimits)

    if "HVAR" in varfont:
        instantiateHVAR(varfont, normalizedLimits)

    if "VVAR" in varfont:
        instantiateVVAR(varfont, normalizedLimits)

    instantiateOTL(varfont, normalizedLimits)

    instantiateFeatureVariations(varfont, normalizedLimits)

    if "avar" in varfont:
        instantiateAvar(varfont, axisLimits)

    with names.pruningUnusedNames(varfont):
        if "STAT" in varfont:
            instantiateSTAT(varfont, axisLimits)

        instantiateFvar(varfont, axisLimits)

    if "OS/2" in varfont:
        varfont["OS/2"].recalcAvgCharWidth(varfont)

    varLib.set_default_weight_width_slant(
        varfont, location=axisLimits.defaultLocation()
    )

    if updateFontNames:
        # Set Regular/Italic/Bold/Bold Italic bits as appropriate, after the
        # name table has been updated.
        setRibbiBits(varfont)

    if downgradeCFF2:
        origVarfont = varfont
        varfont = downgradeCFF2ToCFF(varfont)
        if inplace:
            origVarfont.__dict__ = varfont.__dict__.copy()

    if "fvar" not in varfont:
        if overlap == OverlapMode.KEEP_AND_SET_FLAGS:
            if "glyf" in varfont:
                setMacOverlapFlags(varfont["glyf"])
        elif overlap in (OverlapMode.REMOVE, OverlapMode.REMOVE_AND_IGNORE_ERRORS):
            from fontTools.ttLib.removeOverlaps import removeOverlaps

            log.info("Removing glyph outlines overlaps")
            removeOverlaps(
                varfont,
                ignoreErrors=(overlap == OverlapMode.REMOVE_AND_IGNORE_ERRORS),
            )

    return varfont

