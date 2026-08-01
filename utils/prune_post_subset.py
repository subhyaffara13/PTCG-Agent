
def prune_post_subset(self, ttfFont, options):
    cff = self.cff
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings

        # Drop unused FontDictionaries
        if hasattr(font, "FDSelect"):
            sel = font.FDSelect
            indices = _uniq_sort(sel.gidArray)
            sel.gidArray = [indices.index(ss) for ss in sel.gidArray]
            arr = font.FDArray
            arr.items = [arr[i] for i in indices]
            del arr.file, arr.offsets

    # Desubroutinize if asked for
    if options.desubroutinize:
        cff.desubroutinize()

    # Drop hints if not needed
    if not options.hinting:
        self.remove_hints()
    elif not options.desubroutinize:
        self.remove_unused_subroutines()
    return True


def prune_post_subset(self, font, options):
    if self.Value is None:
        assert self.ValueFormat == 0
        return True

    # Shrink ValueFormat
    if self.Format == 1:
        if not options.hinting:
            self.Value.prune_hints()
        self.ValueFormat = self.Value.getEffectiveFormat()
    elif self.Format == 2:
        if None in self.Value:
            assert self.ValueFormat == 0
            assert all(v is None for v in self.Value)
        else:
            if not options.hinting:
                for v in self.Value:
                    v.prune_hints()
            self.ValueFormat = reduce(
                int.__or__, [v.getEffectiveFormat() for v in self.Value], 0
            )

    # Downgrade to Format 1 if all ValueRecords are the same
    if self.Format == 2 and all(v == self.Value[0] for v in self.Value):
        self.Format = 1
        self.Value = self.Value[0] if self.ValueFormat != 0 else None
        del self.ValueCount

    return True


def prune_post_subset(self, font, options):
    if not options.hinting:
        attr1, attr2 = {
            1: ("PairSet", "PairValueRecord"),
            2: ("Class1Record", "Class2Record"),
        }[self.Format]

        self.ValueFormat1 = self.ValueFormat2 = 0
        for row in getattr(self, attr1):
            for r in getattr(row, attr2):
                if r.Value1:
                    r.Value1.prune_hints()
                    self.ValueFormat1 |= r.Value1.getEffectiveFormat()
                if r.Value2:
                    r.Value2.prune_hints()
                    self.ValueFormat2 |= r.Value2.getEffectiveFormat()

    return bool(self.ValueFormat1 | self.ValueFormat2)


def prune_post_subset(self, font, options):
    if not options.hinting:
        for rec in self.EntryExitRecord:
            if rec.EntryAnchor:
                rec.EntryAnchor.prune_hints()
            if rec.ExitAnchor:
                rec.ExitAnchor.prune_hints()
    return True


def prune_post_subset(self, font, options):
    if not options.hinting:
        for m in self.MarkArray.MarkRecord:
            if m.MarkAnchor:
                m.MarkAnchor.prune_hints()
        for b in self.BaseArray.BaseRecord:
            for a in b.BaseAnchor:
                if a:
                    a.prune_hints()
    return True


def prune_post_subset(self, font, options):
    if not options.hinting:
        for m in self.MarkArray.MarkRecord:
            if m.MarkAnchor:
                m.MarkAnchor.prune_hints()
        for l in self.LigatureArray.LigatureAttach:
            if l is None:
                continue
            for c in l.ComponentRecord:
                for a in c.LigatureAnchor:
                    if a:
                        a.prune_hints()
    return True


def prune_post_subset(self, font, options):
    if not options.hinting:
        for m in self.Mark1Array.MarkRecord:
            if m.MarkAnchor:
                m.MarkAnchor.prune_hints()
        for b in self.Mark2Array.Mark2Record:
            for m in b.Mark2Anchor:
                if m:
                    m.prune_hints()
    return True


def prune_post_subset(self, font, options):
    return True


def prune_post_subset(self, font, options):
    if self.Format == 1:
        return self.ExtSubTable.prune_post_subset(font, options)
    else:
        assert 0, "unknown format: %s" % self.Format


def prune_post_subset(self, font, options):
    ret = False
    for st in self.SubTable:
        if not st:
            continue
        if st.prune_post_subset(font, options):
            ret = True
    return ret


def prune_post_subset(self, font, options):
    ret = False
    for l in self.Lookup:
        if not l:
            continue
        if l.prune_post_subset(font, options):
            ret = True
    return ret


def prune_post_subset(self, font, options):
    table = self.table

    self.prune_lookups()  # XXX Is this actually needed?!

    if table.LookupList:
        table.LookupList.prune_post_subset(font, options)
        # XXX Next two lines disabled because OTS is stupid and
        # doesn't like NULL offsets here.
        # if not table.LookupList.Lookup:
        # 	table.LookupList = None

    if not table.LookupList:
        table.FeatureList = None

    if table.FeatureList:
        self.remove_redundant_langsys()
        # Remove unreferenced features
        self.prune_features()

    # XXX Next two lines disabled because OTS is stupid and
    # doesn't like NULL offsets here.
    # if table.FeatureList and not table.FeatureList.FeatureRecord:
    # 	table.FeatureList = None

    # Never drop scripts themselves as them just being available
    # holds semantic significance.
    # XXX Next two lines disabled because OTS is stupid and
    # doesn't like NULL offsets here.
    # if table.ScriptList and not table.ScriptList.ScriptRecord:
    # 	table.ScriptList = None

    if hasattr(table, "FeatureVariations"):
        # drop FeatureVariations if there are no features to substitute
        if table.FeatureVariations and not (
            table.FeatureList and table.FeatureVariations.FeatureVariationRecord
        ):
            table.FeatureVariations = None

        # downgrade table version if there are no FeatureVariations
        if not table.FeatureVariations and table.Version == 0x00010001:
            table.Version = 0x00010000

    return True


def prune_post_subset(self, font, options):
    table = self.table
    # XXX check these against OTS
    if table.LigCaretList and not table.LigCaretList.LigGlyphCount:
        table.LigCaretList = None
    if table.MarkAttachClassDef and not table.MarkAttachClassDef.classDefs:
        table.MarkAttachClassDef = None
    if table.GlyphClassDef and not table.GlyphClassDef.classDefs:
        table.GlyphClassDef = None
    if table.AttachList and not table.AttachList.GlyphCount:
        table.AttachList = None
    if hasattr(table, "VarStore"):
        _pruneGDEF(font)
        if table.VarStore.VarDataCount == 0:
            if table.Version == 0x00010003:
                table.Version = 0x00010002
    if (
        not hasattr(table, "MarkGlyphSetsDef")
        or not table.MarkGlyphSetsDef
        or not table.MarkGlyphSetsDef.Coverage
    ):
        table.MarkGlyphSetsDef = None
        if table.Version == 0x00010002:
            table.Version = 0x00010000
    return bool(
        table.LigCaretList
        or table.MarkAttachClassDef
        or table.GlyphClassDef
        or table.AttachList
        or (table.Version >= 0x00010002 and table.MarkGlyphSetsDef)
        or (table.Version >= 0x00010003 and table.VarStore)
    )


def prune_post_subset(self, font, options):
    # Keep whole "CPAL" if "SVG " is present as it may be referenced by the latter
    # via 'var(--color{palette_entry_index}, ...)' CSS color variables.
    # For now we just assume this is the case by the mere presence of "SVG " table,
    # for parsing SVG to collect all the used indices is too much work...
    # TODO(anthrotype): Do The Right Thing (TM).
    if "SVG " in font:
        return True

    colr = font.get("COLR")
    if not colr:  # drop CPAL if COLR was subsetted to empty
        return False

    colors_by_index = defaultdict(list)

    def collect_colors_by_index(paint):
        if hasattr(paint, "PaletteIndex"):  # either solid colors...
            colors_by_index[paint.PaletteIndex].append(paint)
        elif hasattr(paint, "ColorLine"):  # ... or gradient color stops
            for stop in paint.ColorLine.ColorStop:
                colors_by_index[stop.PaletteIndex].append(stop)

    if colr.version == 0:
        for layers in colr.ColorLayers.values():
            for layer in layers:
                colors_by_index[layer.colorID].append(layer)
    else:
        if colr.table.LayerRecordArray:
            for layer in colr.table.LayerRecordArray.LayerRecord:
                colors_by_index[layer.PaletteIndex].append(layer)
        for record in colr.table.BaseGlyphList.BaseGlyphPaintRecord:
            record.Paint.traverse(colr.table, collect_colors_by_index)

    # don't remap palette entry index 0xFFFF, this is always the foreground color
    # https://github.com/fonttools/fonttools/issues/2257
    retained_palette_indices = set(colors_by_index.keys()) - {0xFFFF}
    for palette in self.palettes:
        palette[:] = [c for i, c in enumerate(palette) if i in retained_palette_indices]
        assert len(palette) == len(retained_palette_indices)

    for new_index, old_index in enumerate(sorted(retained_palette_indices)):
        for record in colors_by_index[old_index]:
            if hasattr(record, "colorID"):  # v0
                record.colorID = new_index
            elif hasattr(record, "PaletteIndex"):  # v1
                record.PaletteIndex = new_index
            else:
                raise AssertionError(record)

    self.numPaletteEntries = len(self.palettes[0])

    if self.version == 1:
        kept_labels = []
        for i, label in enumerate(self.paletteEntryLabels):
            if i in retained_palette_indices:
                kept_labels.append(label)
        self.paletteEntryLabels = kept_labels
    return bool(self.numPaletteEntries)


def prune_post_subset(self, font, options):
    table = self.table

    store = table.MultiVarStore
    if store is not None:
        usedVarIdxes = set()
        table.collect_varidxes(usedVarIdxes)
        varidx_map = store.subset_varidxes(usedVarIdxes)
        table.remap_varidxes(varidx_map)

    axisIndicesList = table.AxisIndicesList.Item
    if axisIndicesList is not None:
        usedIndices = set()
        for glyph in table.VarCompositeGlyphs.VarCompositeGlyph:
            for comp in glyph.components:
                if comp.axisIndicesIndex is not None:
                    usedIndices.add(comp.axisIndicesIndex)
        usedIndices = sorted(usedIndices)
        table.AxisIndicesList.Item = _list_subset(axisIndicesList, usedIndices)
        mapping = {old: new for new, old in enumerate(usedIndices)}
        for glyph in table.VarCompositeGlyphs.VarCompositeGlyph:
            for comp in glyph.components:
                if comp.axisIndicesIndex is not None:
                    comp.axisIndicesIndex = mapping[comp.axisIndicesIndex]

    conditionList = table.ConditionList
    if conditionList is not None:
        conditionTables = conditionList.ConditionTable
        usedIndices = set()
        for glyph in table.VarCompositeGlyphs.VarCompositeGlyph:
            for comp in glyph.components:
                if comp.conditionIndex is not None:
                    usedIndices.add(comp.conditionIndex)
        usedIndices = sorted(usedIndices)
        conditionList.ConditionTable = _list_subset(conditionTables, usedIndices)
        mapping = {old: new for new, old in enumerate(usedIndices)}
        for glyph in table.VarCompositeGlyphs.VarCompositeGlyph:
            for comp in glyph.components:
                if comp.conditionIndex is not None:
                    comp.conditionIndex = mapping[comp.conditionIndex]

    return True


def prune_post_subset(self, font, options):
    remove_hinting = not options.hinting
    for v in self.glyphs.values():
        v.trim(remove_hinting=remove_hinting)
    return True


def prune_post_subset(self, font, options):
    visitor = NameRecordVisitor()
    visitor.visit(font)
    nameIDs = set(options.name_IDs) | visitor.seen
    if "*" in options.name_IDs:
        nameIDs |= {n.nameID for n in self.names if n.nameID < 256}
    self.names = [n for n in self.names if n.nameID in nameIDs]
    if not options.name_legacy:
        # TODO(behdad) Sometimes (eg Apple Color Emoji) there's only a macroman
        # entry for Latin and no Unicode names.
        self.names = [n for n in self.names if n.isUnicode()]
    # TODO(behdad) Option to keep only one platform's
    if "*" not in options.name_languages:
        # TODO(behdad) This is Windows-platform specific!
        self.names = [n for n in self.names if n.langID in options.name_languages]
    if options.obfuscate_names:
        namerecs = []
        # Preserve names to be scrambled or dropped elsewhere so that other
        # parts of the font don't break.
        needRemapping = visitor.seen.intersection(NAME_IDS_TO_OBFUSCATE)
        if needRemapping:
            _remap_select_name_ids(font, needRemapping)
        for n in self.names:
            if n.nameID in [1, 4]:
                n.string = ".\x7f".encode("utf_16_be") if n.isUnicode() else ".\x7f"
            elif n.nameID in [2, 6]:
                n.string = "\x7f".encode("utf_16_be") if n.isUnicode() else "\x7f"
            elif n.nameID == 3:
                n.string = ""
            elif n.nameID in [16, 17, 18]:
                continue
            namerecs.append(n)
        self.names = namerecs
    return True  # Required table


def prune_post_subset(self, font, options):
    # Force re-compiling head table, to update any recalculated values.
    return True

