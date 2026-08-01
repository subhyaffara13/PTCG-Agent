
def visit(
    path: str | os.PathLike[str], recurse: Callable[[os.DirEntry[str]], bool]
) -> Iterator[os.DirEntry[str]]:
    """Walk a directory recursively, in breadth-first order.

    The `recurse` predicate determines whether a directory is recursed.

    Entries at each directory level are sorted.
    """
    entries = scandir(path)
    yield from entries
    for entry in entries:
        if entry.is_dir() and recurse(entry):
            yield from visit(entry.path, recurse)


def visit(visitor, obj, attr, value):
    setattr(obj, attr, visitor.scale(value))


def visit(visitor, obj, attr, metrics):
    for g in metrics:
        advance, lsb = metrics[g]
        metrics[g] = visitor.scale(advance), visitor.scale(lsb)


def visit(visitor, obj, attr, VOriginRecords):
    for g in VOriginRecords:
        VOriginRecords[g] = visitor.scale(VOriginRecords[g])


def visit(visitor, obj, attr, glyphs):
    for g in glyphs.values():
        for attr in ("xMin", "xMax", "yMin", "yMax"):
            v = getattr(g, attr, None)
            if v is not None:
                setattr(g, attr, visitor.scale(v))

        if g.isComposite():
            for component in g.components:
                component.x = visitor.scale(component.x)
                component.y = visitor.scale(component.y)
            continue

        if hasattr(g, "coordinates"):
            coordinates = g.coordinates
            for i, (x, y) in enumerate(coordinates):
                coordinates[i] = visitor.scale(x), visitor.scale(y)


def visit(visitor, obj, attr, variations):
    glyfTable = visitor.font["glyf"]

    for glyphName, varlist in variations.items():
        glyph = glyfTable[glyphName]
        for var in varlist:
            coordinates = var.coordinates
            for i, xy in enumerate(coordinates):
                if xy is None:
                    continue
                coordinates[i] = visitor.scale(xy[0]), visitor.scale(xy[1])


def visit(visitor, obj, attr, varc):
    # VarComposite variations are a pain

    fvar = visitor.font["fvar"]
    fvarAxes = [a.axisTag for a in fvar.axes]

    store = varc.MultiVarStore
    storeBuilder = OnlineMultiVarStoreBuilder(fvarAxes)

    for g in varc.VarCompositeGlyphs.VarCompositeGlyph:
        for component in g.components:
            t = component.transform
            t.translateX = visitor.scale(t.translateX)
            t.translateY = visitor.scale(t.translateY)
            t.tCenterX = visitor.scale(t.tCenterX)
            t.tCenterY = visitor.scale(t.tCenterY)

            if component.axisValuesVarIndex != otTables.NO_VARIATION_INDEX:
                varIdx = component.axisValuesVarIndex
                # TODO Move this code duplicated below to MultiVarStore.__getitem__,
                # or a getDeltasAndSupports().
                if varIdx != otTables.NO_VARIATION_INDEX:
                    major = varIdx >> 16
                    minor = varIdx & 0xFFFF
                    varData = store.MultiVarData[major]
                    vec = varData.Item[minor]
                    storeBuilder.setSupports(store.get_supports(major, fvar.axes))
                    if vec:
                        m = len(vec) // varData.VarRegionCount
                        vec = list(batched(vec, m))
                        vec = [Vector(v) for v in vec]
                        component.axisValuesVarIndex = storeBuilder.storeDeltas(vec)
                    else:
                        component.axisValuesVarIndex = otTables.NO_VARIATION_INDEX

            if component.transformVarIndex != otTables.NO_VARIATION_INDEX:
                varIdx = component.transformVarIndex
                if varIdx != otTables.NO_VARIATION_INDEX:
                    major = varIdx >> 16
                    minor = varIdx & 0xFFFF
                    vec = varData.Item[varIdx & 0xFFFF]
                    major = varIdx >> 16
                    minor = varIdx & 0xFFFF
                    varData = store.MultiVarData[major]
                    vec = varData.Item[minor]
                    storeBuilder.setSupports(store.get_supports(major, fvar.axes))
                    if vec:
                        m = len(vec) // varData.VarRegionCount
                        flags = component.flags
                        vec = list(batched(vec, m))
                        newVec = []
                        for v in vec:
                            v = list(v)
                            i = 0
                            ## Scale translate & tCenter
                            if flags & otTables.VarComponentFlags.HAVE_TRANSLATE_X:
                                v[i] = visitor.scale(v[i])
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_TRANSLATE_Y:
                                v[i] = visitor.scale(v[i])
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_ROTATION:
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_SCALE_X:
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_SCALE_Y:
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_SKEW_X:
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_SKEW_Y:
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_TCENTER_X:
                                v[i] = visitor.scale(v[i])
                                i += 1
                            if flags & otTables.VarComponentFlags.HAVE_TCENTER_Y:
                                v[i] = visitor.scale(v[i])
                                i += 1

                            newVec.append(Vector(v))
                        vec = newVec

                        component.transformVarIndex = storeBuilder.storeDeltas(vec)
                    else:
                        component.transformVarIndex = otTables.NO_VARIATION_INDEX

    varc.MultiVarStore = storeBuilder.finish()


def visit(visitor, obj, attr, kernTables):
    for table in kernTables:
        kernTable = table.kernTable
        for k in kernTable.keys():
            kernTable[k] = visitor.scale(kernTable[k])


def visit(visitor, obj, attr, cff):
    cff.desubroutinize()
    topDict = cff.topDictIndex[0]
    varStore = getattr(topDict, "VarStore", None)
    getNumRegions = varStore.getNumRegions if varStore is not None else None
    privates = set()
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings
        for g in font.charset:
            c, _ = cs.getItemAndSelector(g)
            privates.add(c.private)

            commands = cffSpecializer.programToCommands(
                c.program, getNumRegions=getNumRegions
            )
            for op, args in commands:
                if op == "vsindex":
                    continue
                _cff_scale(visitor, args)
            c.program[:] = cffSpecializer.commandsToProgram(commands)

        # Annoying business of scaling numbers that do not matter whatsoever

        for attr in (
            "UnderlinePosition",
            "UnderlineThickness",
            "FontBBox",
            "StrokeWidth",
        ):
            value = getattr(topDict, attr, None)
            if value is None:
                continue
            if isinstance(value, list):
                _cff_scale(visitor, value)
            else:
                setattr(topDict, attr, visitor.scale(value))

        for i in range(6):
            topDict.FontMatrix[i] /= visitor.scaleFactor

        for private in privates:
            for attr in (
                "BlueValues",
                "OtherBlues",
                "FamilyBlues",
                "FamilyOtherBlues",
                # "BlueScale",
                # "BlueShift",
                # "BlueFuzz",
                "StdHW",
                "StdVW",
                "StemSnapH",
                "StemSnapV",
                "defaultWidthX",
                "nominalWidthX",
            ):
                value = getattr(private, attr, None)
                if value is None:
                    continue
                if isinstance(value, list):
                    _cff_scale(visitor, value)
                else:
                    setattr(private, attr, visitor.scale(value))


def visit(visitor, varData):
    for item in varData.Item:
        for i, v in enumerate(item):
            item[i] = visitor.scale(v)
    varData.calculateNumShorts()


def visit(visitor, record):
    oldPaint = record.Paint

    scale = otTables.Paint()
    _setup_scale_paint(scale, visitor.scaleFactor)
    scale.Paint = oldPaint

    record.Paint = scale

    return True


def visit(visitor, paint):
    if paint.Format != otTables.PaintFormat.PaintGlyph:
        return True

    newPaint = otTables.Paint()
    newPaint.Format = paint.Format
    newPaint.Paint = paint.Paint
    newPaint.Glyph = paint.Glyph
    del paint.Paint
    del paint.Glyph

    _setup_scale_paint(paint, 1 / visitor.scaleFactor)
    paint.Paint = newPaint

    visitor.visit(newPaint.Paint)

    return False


def visit(visitor, font, *args, **kwargs):
    # Some objects have links back to TTFont; even though we
    # have a check in visitAttr to stop them from recursing
    # onto TTFont, sometimes they still do, for example when
    # someone overrides visitAttr.
    if hasattr(visitor, "font"):
        return False

    visitor.font = font
    for tag in font.keys():
        visitor.visit(font[tag], *args, **kwargs)
    del visitor.font
    return False


def visit(visitor, obj, attr, value):
    shift = visitor.shift
    value = [l + shift for l in value]
    setattr(obj, attr, value)


def visit(visitor, obj, attr, value):
    setattr(obj, attr, visitor.shift + value)


def visit(visitor, obj, attr, value):
    visitor.seen.add(value)


def visit(visitor, obj):
    for attr in ("FeatUILabelNameID", "FeatUITooltipTextNameID", "SampleTextNameID"):
        value = getattr(obj, attr)
        visitor.seen.add(value)
    # also include the sequence of UI strings for individual variants, if any
    if obj.FirstParamUILabelNameID == 0 or obj.NumNamedParameters == 0:
        return
    visitor.seen.update(
        range(
            obj.FirstParamUILabelNameID,
            obj.FirstParamUILabelNameID + obj.NumNamedParameters,
        )
    )


def visit(visitor, obj):
    for inst in obj.instances:
        if inst.postscriptNameID != 0xFFFF:
            visitor.seen.add(inst.postscriptNameID)
        visitor.seen.add(inst.subfamilyNameID)

    for axis in obj.axes:
        visitor.seen.add(axis.axisNameID)


def visit(visitor, obj):
    if obj.version == 1:
        visitor.seen.update(obj.paletteLabels)
        visitor.seen.update(obj.paletteEntryLabels)


def visit(visitor, font, *args, **kwargs):
    if hasattr(visitor, "font"):
        return False

    visitor.font = font
    for tag in visitor.TABLES:
        if tag in font:
            visitor.visit(font[tag], *args, **kwargs)
    del visitor.font
    return False


def visit(hint: TypeForm, leaf_fn: _LeafFn):
  """Recurse in the type annotation tree."""
  origin = typing_extensions.get_origin(hint)
  visit_fn = _ORIGIN_TO_VISITOR.get(origin, _visit_leaf)
  visit_fn(hint, leaf_fn)

