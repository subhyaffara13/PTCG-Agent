from typing import Dict, List

def subset_glyphs(self, s):
    cff = self.cff
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings

        glyphs = s.glyphs.union(s.glyphs_emptied)

        # Load all glyphs
        for g in font.charset:
            if g not in glyphs:
                continue
            c, _ = cs.getItemAndSelector(g)

        if cs.charStringsAreIndexed:
            indices = [i for i, g in enumerate(font.charset) if g in glyphs]
            csi = cs.charStringsIndex
            csi.items = [csi.items[i] for i in indices]
            del csi.file, csi.offsets
            if hasattr(font, "FDSelect"):
                sel = font.FDSelect
                sel.format = None
                sel.gidArray = [sel.gidArray[i] for i in indices]
            newCharStrings = {}
            for indicesIdx, charsetIdx in enumerate(indices):
                g = font.charset[charsetIdx]
                if g in cs.charStrings:
                    newCharStrings[g] = indicesIdx
            cs.charStrings = newCharStrings
        else:
            cs.charStrings = {g: v for g, v in cs.charStrings.items() if g in glyphs}
        font.charset = [g for g in font.charset if g in glyphs]
        font.numGlyphs = len(font.charset)

        if s.options.retain_gids:
            isCFF2 = cff.major > 1
            for g in s.glyphs_emptied:
                _empty_charstring(font, g, isCFF2=isCFF2, ignoreWidth=True)

    return True  # any(cff[fontname].numGlyphs for fontname in cff.keys())


def subset_glyphs(self, s) -> bool:
    if etree is None:
        raise ImportError("No module named 'lxml', required to subset SVG")

    # glyph names (before subsetting)
    glyph_order: List[str] = s.orig_glyph_order
    # map from glyph names to original glyph indices
    rev_orig_glyph_map: Dict[str, int] = s.reverseOrigGlyphMap
    # map from original to new glyph indices (after subsetting)
    glyph_index_map: Dict[int, int] = s.glyph_index_map

    new_docs: List[SVGDocument] = []
    for doc in self.docList:
        glyphs = {
            glyph_order[i] for i in range(doc.startGlyphID, doc.endGlyphID + 1)
        }.intersection(s.glyphs)
        if not glyphs:
            # no intersection: we can drop the whole record
            continue

        svg = etree.fromstring(
            # encode because fromstring dislikes xml encoding decl if input is str.
            # SVG xml encoding must be utf-8 as per OT spec.
            doc.data.encode("utf-8"),
            parser=etree.XMLParser(
                # Disable libxml2 security restrictions to support very deep trees.
                # Without this we would get an error like this:
                # `lxml.etree.XMLSyntaxError: internal error: Huge input lookup`
                # when parsing big fonts e.g. noto-emoji-picosvg.ttf.
                huge_tree=True,
                # ignore blank text as it's not meaningful in OT-SVG; it also prevents
                # dangling tail text after removing an element when pretty_print=True
                remove_blank_text=True,
                # don't replace entities; we don't expect any in OT-SVG and they may
                # be abused for XXE attacks
                resolve_entities=False,
            ),
        )

        elements = group_elements_by_id(svg)
        gids = {rev_orig_glyph_map[g] for g in glyphs}
        element_ids = {f"glyph{i}" for i in gids}
        closure_element_ids(elements, element_ids)

        if not subset_elements(svg, element_ids):
            continue

        if not s.options.retain_gids:
            id_map = remap_glyph_ids(svg, glyph_index_map)
            update_glyph_href_links(svg, id_map)

        new_doc = etree.tostring(svg, pretty_print=s.options.pretty_svg).decode("utf-8")

        new_gids = (glyph_index_map[i] for i in gids)
        for start, end in ranges(new_gids):
            new_docs.append(SVGDocument(new_doc, start, end, doc.compressed))

    self.docList = new_docs

    return bool(self.docList)


def subset_glyphs(self, s):
    self.mapping = {
        g: v for g, v in self.mapping.items() if g in s.glyphs and v in s.glyphs
    }
    return bool(self.mapping)


def subset_glyphs(self, s):
    self.mapping = {
        g: v
        for g, v in self.mapping.items()
        if g in s.glyphs and all(sub in s.glyphs for sub in v)
    }
    return bool(self.mapping)


def subset_glyphs(self, s):
    self.alternates = {
        g: [v for v in vlist if v in s.glyphs]
        for g, vlist in self.alternates.items()
        if g in s.glyphs and any(v in s.glyphs for v in vlist)
    }
    return bool(self.alternates)


def subset_glyphs(self, s):
    self.ligatures = {g: v for g, v in self.ligatures.items() if g in s.glyphs}
    self.ligatures = {
        g: [
            seq
            for seq in seqs
            if seq.LigGlyph in s.glyphs and all(c in s.glyphs for c in seq.Component)
        ]
        for g, seqs in self.ligatures.items()
    }
    self.ligatures = {g: v for g, v in self.ligatures.items() if v}
    return bool(self.ligatures)


def subset_glyphs(self, s):
    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        self.Substitute = _list_subset(self.Substitute, indices)
        # Now drop rules generating glyphs we don't want
        indices = [i for i, sub in enumerate(self.Substitute) if sub in s.glyphs]
        self.Substitute = _list_subset(self.Substitute, indices)
        self.Coverage.remap(indices)
        self.GlyphCount = len(self.Substitute)
        return bool(
            self.GlyphCount
            and all(
                c.subset(s.glyphs)
                for c in self.LookAheadCoverage + self.BacktrackCoverage
            )
        )
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        return len(self.Coverage.subset(s.glyphs))
    elif self.Format == 2:
        indices = self.Coverage.subset(s.glyphs)
        values = self.Value
        count = len(values)
        self.Value = [values[i] for i in indices if i < count]
        self.ValueCount = len(self.Value)
        return bool(self.ValueCount)
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        pairs = self.PairSet
        count = len(pairs)
        self.PairSet = [pairs[i] for i in indices if i < count]
        for p in self.PairSet:
            p.PairValueRecord = [
                r for r in p.PairValueRecord if r.SecondGlyph in s.glyphs
            ]
            p.PairValueCount = len(p.PairValueRecord)
        # Remove empty pairsets
        indices = [i for i, p in enumerate(self.PairSet) if p.PairValueCount]
        self.Coverage.remap(indices)
        self.PairSet = _list_subset(self.PairSet, indices)
        self.PairSetCount = len(self.PairSet)
        return bool(self.PairSetCount)
    elif self.Format == 2:
        class1_map = [
            c
            for c in self.ClassDef1.subset(
                s.glyphs.intersection(self.Coverage.glyphs), remap=True
            )
            if c < self.Class1Count
        ]
        class2_map = [
            c
            for c in self.ClassDef2.subset(s.glyphs, remap=True, useClass0=False)
            if c < self.Class2Count
        ]
        self.Class1Record = [self.Class1Record[i] for i in class1_map]
        for c in self.Class1Record:
            c.Class2Record = [c.Class2Record[i] for i in class2_map]
        self.Class1Count = len(class1_map)
        self.Class2Count = len(class2_map)
        # If only Class2 0 left, no need to keep anything.
        return bool(
            self.Class1Count
            and (self.Class2Count > 1)
            and self.Coverage.subset(s.glyphs)
        )
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        records = self.EntryExitRecord
        count = len(records)
        self.EntryExitRecord = [records[i] for i in indices if i < count]
        self.EntryExitCount = len(self.EntryExitRecord)
        return bool(self.EntryExitCount)
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        mark_indices = self.MarkCoverage.subset(s.glyphs)
        self.MarkArray.MarkRecord = _list_subset(
            self.MarkArray.MarkRecord, mark_indices
        )
        self.MarkArray.MarkCount = len(self.MarkArray.MarkRecord)
        class_indices = _uniq_sort(v.Class for v in self.MarkArray.MarkRecord)

        intersect_base_indices = self.BaseCoverage.intersect(s.glyphs)
        base_records = self.BaseArray.BaseRecord
        num_base_records = len(base_records)
        base_indices = [
            i
            for i in intersect_base_indices
            if i < num_base_records
            and any(base_records[i].BaseAnchor[j] is not None for j in class_indices)
        ]
        if not base_indices:
            return False

        self.BaseCoverage.remap(base_indices)
        self.BaseArray.BaseRecord = _list_subset(
            self.BaseArray.BaseRecord, base_indices
        )
        self.BaseArray.BaseCount = len(self.BaseArray.BaseRecord)
        # Prune empty classes
        self.ClassCount = len(class_indices)
        for m in self.MarkArray.MarkRecord:
            m.Class = class_indices.index(m.Class)
        for b in self.BaseArray.BaseRecord:
            b.BaseAnchor = _list_subset(b.BaseAnchor, class_indices)
        return bool(
            self.ClassCount and self.MarkArray.MarkCount and self.BaseArray.BaseCount
        )
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        mark_indices = self.MarkCoverage.subset(s.glyphs)
        self.MarkArray.MarkRecord = _list_subset(
            self.MarkArray.MarkRecord, mark_indices
        )
        self.MarkArray.MarkCount = len(self.MarkArray.MarkRecord)
        class_indices = _uniq_sort(v.Class for v in self.MarkArray.MarkRecord)

        intersect_ligature_indices = self.LigatureCoverage.intersect(s.glyphs)
        ligature_array = self.LigatureArray.LigatureAttach
        num_ligatures = self.LigatureArray.LigatureCount

        ligature_indices = [
            i
            for i in intersect_ligature_indices
            if i < num_ligatures
            and any(
                any(component.LigatureAnchor[j] is not None for j in class_indices)
                for component in ligature_array[i].ComponentRecord
            )
        ]

        if not ligature_indices:
            return False

        self.LigatureCoverage.remap(ligature_indices)
        self.LigatureArray.LigatureAttach = _list_subset(
            self.LigatureArray.LigatureAttach, ligature_indices
        )
        self.LigatureArray.LigatureCount = len(self.LigatureArray.LigatureAttach)
        # Prune empty classes
        self.ClassCount = len(class_indices)
        for m in self.MarkArray.MarkRecord:
            m.Class = class_indices.index(m.Class)
        for l in self.LigatureArray.LigatureAttach:
            if l is None:
                continue
            for c in l.ComponentRecord:
                c.LigatureAnchor = _list_subset(c.LigatureAnchor, class_indices)
        return bool(
            self.ClassCount
            and self.MarkArray.MarkCount
            and self.LigatureArray.LigatureCount
        )
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        mark1_indices = self.Mark1Coverage.subset(s.glyphs)
        self.Mark1Array.MarkRecord = _list_subset(
            self.Mark1Array.MarkRecord, mark1_indices
        )
        self.Mark1Array.MarkCount = len(self.Mark1Array.MarkRecord)
        class_indices = _uniq_sort(v.Class for v in self.Mark1Array.MarkRecord)

        intersect_mark2_indices = self.Mark2Coverage.intersect(s.glyphs)
        mark2_records = self.Mark2Array.Mark2Record
        num_mark2_records = len(mark2_records)
        mark2_indices = [
            i
            for i in intersect_mark2_indices
            if i < num_mark2_records
            and any(mark2_records[i].Mark2Anchor[j] is not None for j in class_indices)
        ]
        if not mark2_indices:
            return False

        self.Mark2Coverage.remap(mark2_indices)
        self.Mark2Array.Mark2Record = _list_subset(
            self.Mark2Array.Mark2Record, mark2_indices
        )
        self.Mark2Array.MarkCount = len(self.Mark2Array.Mark2Record)
        # Prune empty classes
        self.ClassCount = len(class_indices)
        for m in self.Mark1Array.MarkRecord:
            m.Class = class_indices.index(m.Class)
        for b in self.Mark2Array.Mark2Record:
            b.Mark2Anchor = _list_subset(b.Mark2Anchor, class_indices)
        return bool(
            self.ClassCount and self.Mark1Array.MarkCount and self.Mark2Array.MarkCount
        )
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    c = self.__subset_classify_context()

    if self.Format == 1:
        indices = self.Coverage.subset(s.glyphs)
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        rss = [rss[i] for i in indices if i < rssCount]
        for rs in rss:
            if not rs:
                continue
            ss = getattr(rs, c.Rule)
            ss = [
                r
                for r in ss
                if r
                and all(all(g in s.glyphs for g in glist) for glist in c.RuleData(r))
            ]
            setattr(rs, c.Rule, ss)
            setattr(rs, c.RuleCount, len(ss))
        # Prune empty rulesets
        indices = [i for i, rs in enumerate(rss) if rs and getattr(rs, c.Rule)]
        self.Coverage.remap(indices)
        rss = _list_subset(rss, indices)
        setattr(self, c.RuleSet, rss)
        setattr(self, c.RuleSetCount, len(rss))
        return bool(rss)
    elif self.Format == 2:
        if not self.Coverage.subset(s.glyphs):
            return False
        ContextData = c.ContextData(self)
        klass_maps = [
            x.subset(s.glyphs, remap=True) if x else None for x in ContextData
        ]

        # Keep rulesets for class numbers that survived.
        indices = klass_maps[c.ClassDefIndex]
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        rss = [rss[i] for i in indices if i < rssCount]
        del rssCount
        # Delete, but not renumber, unreachable rulesets.
        indices = getattr(self, c.ClassDef).intersect(self.Coverage.glyphs)
        rss = [rss if i in indices else None for i, rss in enumerate(rss)]

        for rs in rss:
            if not rs:
                continue
            ss = getattr(rs, c.Rule)
            ss = [
                r
                for r in ss
                if r
                and all(
                    all(k in klass_map for k in klist)
                    for klass_map, klist in zip(klass_maps, c.RuleData(r))
                )
            ]
            setattr(rs, c.Rule, ss)
            setattr(rs, c.RuleCount, len(ss))

            # Remap rule classes
            for r in ss:
                c.SetRuleData(
                    r,
                    [
                        [klass_map.index(k) for k in klist]
                        for klass_map, klist in zip(klass_maps, c.RuleData(r))
                    ],
                )

        # Prune empty rulesets
        rss = [rs if rs and getattr(rs, c.Rule) else None for rs in rss]
        while rss and rss[-1] is None:
            del rss[-1]
        setattr(self, c.RuleSet, rss)
        setattr(self, c.RuleSetCount, len(rss))

        # TODO: We can do a second round of remapping class values based
        # on classes that are actually used in at least one rule.	Right
        # now we subset classes to c.glyphs only.	Or better, rewrite
        # the above to do that.

        return bool(rss)
    elif self.Format == 3:
        return all(x is not None and x.subset(s.glyphs) for x in c.RuleData(self))
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    if self.Format == 1:
        return self.ExtSubTable.subset_glyphs(s)
    else:
        assert 0, "unknown format: %s" % self.Format


def subset_glyphs(self, s):
    self.SubTable = [st for st in self.SubTable if st and st.subset_glyphs(s)]
    self.SubTableCount = len(self.SubTable)
    if hasattr(self, "MarkFilteringSet") and self.MarkFilteringSet is not None:
        if self.MarkFilteringSet not in s.used_mark_sets:
            self.MarkFilteringSet = None
            self.LookupFlag &= ~0x10
            self.LookupFlag |= 0x8
        else:
            self.MarkFilteringSet = s.used_mark_sets.index(self.MarkFilteringSet)
    return bool(self.SubTableCount)


def subset_glyphs(self, s):
    """Returns the indices of nonempty lookups."""
    return [i for i, l in enumerate(self.Lookup) if l and l.subset_glyphs(s)]


def subset_glyphs(self, s):
    for strike in self.strikes:
        for indexSubTable in strike.indexSubTables:
            indexSubTable.names = [n for n in indexSubTable.names if n in s.glyphs]
        strike.indexSubTables = [i for i in strike.indexSubTables if i.names]
    self.strikes = [s for s in self.strikes if s.indexSubTables]

    return True


def subset_glyphs(self, s):
    strikeData = [
        {g: strike[g] for g in s.glyphs if g in strike} for strike in self.strikeData
    ]
    # Prune empty strikes
    # https://github.com/fonttools/fonttools/issues/1633
    self.strikeData = [strike for strike in strikeData if strike]
    return True


def subset_glyphs(self, s):
    for strike in self.strikes.values():
        strike.glyphs = {g: strike.glyphs[g] for g in s.glyphs if g in strike.glyphs}

    return True


def subset_glyphs(self, s):
    s.glyphs = s.glyphs_gsubed
    if self.table.LookupList:
        lookup_indices = self.table.LookupList.subset_glyphs(s)
    else:
        lookup_indices = []
    self.subset_lookups(lookup_indices)
    return True


def subset_glyphs(self, s):
    glyphs = s.glyphs_gsubed
    table = self.table
    if table.LigCaretList:
        indices = table.LigCaretList.Coverage.subset(glyphs)
        table.LigCaretList.LigGlyph = _list_subset(table.LigCaretList.LigGlyph, indices)
        table.LigCaretList.LigGlyphCount = len(table.LigCaretList.LigGlyph)
    if table.MarkAttachClassDef:
        table.MarkAttachClassDef.classDefs = {
            g: v for g, v in table.MarkAttachClassDef.classDefs.items() if g in glyphs
        }
    if table.GlyphClassDef:
        table.GlyphClassDef.classDefs = {
            g: v for g, v in table.GlyphClassDef.classDefs.items() if g in glyphs
        }
    if table.AttachList:
        indices = table.AttachList.Coverage.subset(glyphs)
        GlyphCount = table.AttachList.GlyphCount
        table.AttachList.AttachPoint = [
            table.AttachList.AttachPoint[i] for i in indices if i < GlyphCount
        ]
        table.AttachList.GlyphCount = len(table.AttachList.AttachPoint)
    if hasattr(table, "MarkGlyphSetsDef") and table.MarkGlyphSetsDef:
        markGlyphSets = table.MarkGlyphSetsDef
        for coverage in markGlyphSets.Coverage:
            if coverage:
                coverage.subset(glyphs)

        s.used_mark_sets = [i for i, c in enumerate(markGlyphSets.Coverage) if c.glyphs]
        markGlyphSets.Coverage = [c for c in markGlyphSets.Coverage if c.glyphs]

    return True


def subset_glyphs(self, s):
    glyphs = s.glyphs_gsubed
    for t in self.kernTables:
        t.kernTable = {
            (a, b): v
            for (a, b), v in t.kernTable.items()
            if a in glyphs and b in glyphs
        }
    self.kernTables = [t for t in self.kernTables if t.kernTable]
    return bool(self.kernTables)


def subset_glyphs(self, s):
    self.metrics = _dict_subset(self.metrics, s.glyphs)
    for g in s.glyphs_emptied:
        self.metrics[g] = (0, 0)
    return bool(self.metrics)


def subset_glyphs(self, s):
    self.metrics = _dict_subset(self.metrics, s.glyphs)
    for g in s.glyphs_emptied:
        self.metrics[g] = (0, 0)
    return True  # Required table


def subset_glyphs(self, s):
    self.hdmx = {sz: _dict_subset(l, s.glyphs) for sz, l in self.hdmx.items()}
    for sz in self.hdmx:
        for g in s.glyphs_emptied:
            self.hdmx[sz][g] = 0
    return bool(self.hdmx)


def subset_glyphs(self, s):
    table = self.table.AnchorPoints
    assert table.Format == 0, "unknown 'ankr' format %s" % table.Format
    table.Anchors = {
        glyph: table.Anchors[glyph] for glyph in s.glyphs if glyph in table.Anchors
    }
    return len(table.Anchors) > 0


def subset_glyphs(self, s):
    table = self.table.Baseline
    if table.Format in (1, 3):
        baselines = {
            glyph: table.BaselineValues.get(glyph, table.DefaultBaseline)
            for glyph in s.glyphs
        }
        if len(baselines) > 0:
            mostCommon, _cnt = Counter(baselines.values()).most_common(1)[0]
            table.DefaultBaseline = mostCommon
            baselines = {glyph: b for glyph, b in baselines.items() if b != mostCommon}
        if len(baselines) > 0:
            table.BaselineValues = baselines
        else:
            table.Format = {1: 0, 3: 2}[table.Format]
            del table.BaselineValues
    return True


def subset_glyphs(self, s):
    table = self.table.LigatureCarets
    if table.Format in (0, 1):
        table.Carets = {
            glyph: table.Carets[glyph] for glyph in s.glyphs if glyph in table.Carets
        }
        return len(table.Carets) > 0
    else:
        assert False, "unknown 'lcar' format %s" % table.Format


def subset_glyphs(self, s):
    self.variations = _dict_subset(self.variations, s.glyphs)
    self.glyphCount = len(self.variations)
    return bool(self.variations)


def subset_glyphs(self, s):
    table = self.table

    used = set()
    advIdxes_ = set()
    retainAdvMap = False

    if table.AdvWidthMap:
        table.AdvWidthMap.mapping = _dict_subset(table.AdvWidthMap.mapping, s.glyphs)
        used.update(table.AdvWidthMap.mapping.values())
    else:
        used.update(s.reverseOrigGlyphMap.values())
        advIdxes_ = used.copy()
        retainAdvMap = s.options.retain_gids

    if table.LsbMap:
        table.LsbMap.mapping = _dict_subset(table.LsbMap.mapping, s.glyphs)
        used.update(table.LsbMap.mapping.values())
    if table.RsbMap:
        table.RsbMap.mapping = _dict_subset(table.RsbMap.mapping, s.glyphs)
        used.update(table.RsbMap.mapping.values())

    varidx_map = table.VarStore.subset_varidxes(
        used, retainFirstMap=retainAdvMap, advIdxes=advIdxes_
    )

    if table.AdvWidthMap:
        table.AdvWidthMap.mapping = _remap_index_map(s, varidx_map, table.AdvWidthMap)
    if table.LsbMap:
        table.LsbMap.mapping = _remap_index_map(s, varidx_map, table.LsbMap)
    if table.RsbMap:
        table.RsbMap.mapping = _remap_index_map(s, varidx_map, table.RsbMap)

    # TODO Return emptiness...
    return True


def subset_glyphs(self, s):
    table = self.table

    used = set()
    advIdxes_ = set()
    retainAdvMap = False

    if table.AdvHeightMap:
        table.AdvHeightMap.mapping = _dict_subset(table.AdvHeightMap.mapping, s.glyphs)
        used.update(table.AdvHeightMap.mapping.values())
    else:
        used.update(s.reverseOrigGlyphMap.values())
        advIdxes_ = used.copy()
        retainAdvMap = s.options.retain_gids

    if table.TsbMap:
        table.TsbMap.mapping = _dict_subset(table.TsbMap.mapping, s.glyphs)
        used.update(table.TsbMap.mapping.values())
    if table.BsbMap:
        table.BsbMap.mapping = _dict_subset(table.BsbMap.mapping, s.glyphs)
        used.update(table.BsbMap.mapping.values())
    if table.VOrgMap:
        table.VOrgMap.mapping = _dict_subset(table.VOrgMap.mapping, s.glyphs)
        used.update(table.VOrgMap.mapping.values())

    varidx_map = table.VarStore.subset_varidxes(
        used, retainFirstMap=retainAdvMap, advIdxes=advIdxes_
    )

    if table.AdvHeightMap:
        table.AdvHeightMap.mapping = _remap_index_map(s, varidx_map, table.AdvHeightMap)
    if table.TsbMap:
        table.TsbMap.mapping = _remap_index_map(s, varidx_map, table.TsbMap)
    if table.BsbMap:
        table.BsbMap.mapping = _remap_index_map(s, varidx_map, table.BsbMap)
    if table.VOrgMap:
        table.VOrgMap.mapping = _remap_index_map(s, varidx_map, table.VOrgMap)

    # TODO Return emptiness...
    return True


def subset_glyphs(self, s):
    self.VOriginRecords = {
        g: v for g, v in self.VOriginRecords.items() if g in s.glyphs
    }
    self.numVertOriginYMetrics = len(self.VOriginRecords)
    return True  # Never drop; has default metrics


def subset_glyphs(self, s):
    table = self.table.OpticalBounds
    if table.Format == 0:
        table.OpticalBoundsDeltas = {
            glyph: table.OpticalBoundsDeltas[glyph]
            for glyph in s.glyphs
            if glyph in table.OpticalBoundsDeltas
        }
        return len(table.OpticalBoundsDeltas) > 0
    elif table.Format == 1:
        table.OpticalBoundsPoints = {
            glyph: table.OpticalBoundsPoints[glyph]
            for glyph in s.glyphs
            if glyph in table.OpticalBoundsPoints
        }
        return len(table.OpticalBoundsPoints) > 0
    else:
        assert False, "unknown 'opbd' format %s" % table.Format


def subset_glyphs(self, s):
    self.extraNames = []  # This seems to do it
    return True  # Required table


def subset_glyphs(self, s):
    prop = self.table.GlyphProperties
    if prop.Format == 0:
        return prop.DefaultProperties != 0
    elif prop.Format == 1:
        prop.Properties = {
            g: prop.Properties.get(g, prop.DefaultProperties) for g in s.glyphs
        }
        mostCommon, _cnt = Counter(prop.Properties.values()).most_common(1)[0]
        prop.DefaultProperties = mostCommon
        prop.Properties = {
            g: prop for g, prop in prop.Properties.items() if prop != mostCommon
        }
        if len(prop.Properties) == 0:
            del prop.Properties
            prop.Format = 0
            return prop.DefaultProperties != 0
        return True
    else:
        assert False, "unknown 'prop' format %s" % prop.Format


def subset_glyphs(self, s):
    from fontTools.colorLib.unbuilder import unbuildColrV1
    from fontTools.colorLib.builder import buildColrV1, populateCOLRv0

    # only include glyphs after COLR closure, which in turn comes after cmap and GSUB
    # closure, but importantly before glyf/CFF closures. COLR layers can refer to
    # composite glyphs, and that's ok, since glyf/CFF closures happen after COLR closure
    # and take care of those. If we also included glyphs resulting from glyf/CFF closures
    # when deciding which COLR base glyphs to retain, then we may end up with a situation
    # whereby a COLR base glyph is kept, not because directly requested (cmap)
    # or substituted (GSUB) or referenced by another COLRv1 PaintColrGlyph, but because
    # it corresponds to (has same GID as) a non-COLR glyph that happens to be used as a
    # component in glyf or CFF table. Best case scenario we retain more glyphs than
    # required; worst case we retain incomplete COLR records that try to reference
    # glyphs that are no longer in the final subset font.
    # https://github.com/fonttools/fonttools/issues/2461
    s.glyphs = s.glyphs_colred

    self.ColorLayers = {
        g: self.ColorLayers[g] for g in s.glyphs if g in self.ColorLayers
    }
    if self.version == 0:
        return bool(self.ColorLayers)

    colorGlyphsV1 = unbuildColrV1(self.table.LayerList, self.table.BaseGlyphList)
    self.table.LayerList, self.table.BaseGlyphList = buildColrV1(
        {g: colorGlyphsV1[g] for g in colorGlyphsV1 if g in s.glyphs}
    )
    del self.ColorLayersV1

    if self.table.ClipList is not None:
        clips = self.table.ClipList.clips
        self.table.ClipList.clips = {g: clips[g] for g in clips if g in s.glyphs}

    layersV0 = self.ColorLayers
    if not self.table.BaseGlyphList.BaseGlyphPaintRecord:
        # no more COLRv1 glyphs: downgrade to version 0
        self.version = 0
        del self.table
        return bool(layersV0)

    populateCOLRv0(
        self.table,
        {g: [(layer.name, layer.colorID) for layer in layersV0[g]] for g in layersV0},
    )
    del self.ColorLayers

    # TODO: also prune ununsed varIndices in COLR.VarStore
    return True


def subset_glyphs(self, s):
    indices = self.table.Coverage.subset(s.glyphs)
    self.table.VarCompositeGlyphs.VarCompositeGlyph = _list_subset(
        self.table.VarCompositeGlyphs.VarCompositeGlyph, indices
    )
    return bool(self.table.VarCompositeGlyphs.VarCompositeGlyph)


def subset_glyphs(self, s):
    indices = self.Coverage.subset(s.glyphs)
    self.ItalicsCorrection = _list_subset(self.ItalicsCorrection, indices)
    self.ItalicsCorrectionCount = len(self.ItalicsCorrection)
    return bool(self.ItalicsCorrectionCount)


def subset_glyphs(self, s):
    indices = self.TopAccentCoverage.subset(s.glyphs)
    self.TopAccentAttachment = _list_subset(self.TopAccentAttachment, indices)
    self.TopAccentAttachmentCount = len(self.TopAccentAttachment)
    return bool(self.TopAccentAttachmentCount)


def subset_glyphs(self, s):
    indices = self.MathKernCoverage.subset(s.glyphs)
    self.MathKernInfoRecords = _list_subset(self.MathKernInfoRecords, indices)
    self.MathKernCount = len(self.MathKernInfoRecords)
    return bool(self.MathKernCount)


def subset_glyphs(self, s):
    if self.MathItalicsCorrectionInfo:
        self.MathItalicsCorrectionInfo.subset_glyphs(s)
    if self.MathTopAccentAttachment:
        self.MathTopAccentAttachment.subset_glyphs(s)
    if self.MathKernInfo:
        self.MathKernInfo.subset_glyphs(s)
    if self.ExtendedShapeCoverage:
        self.ExtendedShapeCoverage.subset(s.glyphs)
    return True


def subset_glyphs(self, s):
    if self.VertGlyphCoverage:
        indices = self.VertGlyphCoverage.subset(s.glyphs)
        self.VertGlyphConstruction = _list_subset(self.VertGlyphConstruction, indices)
        self.VertGlyphCount = len(self.VertGlyphConstruction)

    if self.HorizGlyphCoverage:
        indices = self.HorizGlyphCoverage.subset(s.glyphs)
        self.HorizGlyphConstruction = _list_subset(self.HorizGlyphConstruction, indices)
        self.HorizGlyphCount = len(self.HorizGlyphConstruction)

    return True


def subset_glyphs(self, s):
    s.glyphs = s.glyphs_mathed
    if self.table.MathGlyphInfo:
        self.table.MathGlyphInfo.subset_glyphs(s)
    if self.table.MathVariants:
        self.table.MathVariants.subset_glyphs(s)
    return True


def subset_glyphs(self, s):
    self.glyphs = _dict_subset(self.glyphs, s.glyphs)
    if not s.options.retain_gids:
        indices = [i for i, g in enumerate(self.glyphOrder) if g in s.glyphs]
        glyphmap = {o: n for n, o in enumerate(indices)}
        for v in self.glyphs.values():
            if hasattr(v, "data"):
                v.remapComponentsFast(glyphmap)
    Glyph = ttLib.getTableModule("glyf").Glyph
    for g in s.glyphs_emptied:
        self.glyphs[g] = Glyph()
        self.glyphs[g].data = b""
    self.glyphOrder = [
        g for g in self.glyphOrder if g in s.glyphs or g in s.glyphs_emptied
    ]
    # Don't drop empty 'glyf' tables, otherwise 'loca' doesn't get subset.
    return True


def subset_glyphs(self, s):
    s.glyphs = None  # We use s.glyphs_requested and s.unicodes_requested only

    tables_format12_bmp = []
    table_plat0_enc3 = {}  # Unicode platform, Unicode BMP only, keyed by language
    table_plat3_enc1 = {}  # Windows platform, Unicode BMP, keyed by language

    for t in self.tables:
        if t.platformID == 0 and t.platEncID == 3:
            table_plat0_enc3[t.language] = t
        if t.platformID == 3 and t.platEncID == 1:
            table_plat3_enc1[t.language] = t

        if t.format == 14:
            # TODO(behdad) We drop all the default-UVS mappings
            # for glyphs_requested.  So it's the caller's responsibility to make
            # sure those are included.
            t.uvsDict = {
                v: [
                    (u, g)
                    for u, g in l
                    if g in s.glyphs_requested or u in s.unicodes_requested
                ]
                for v, l in t.uvsDict.items()
                if v in s.unicodes_requested
            }
            t.uvsDict = {v: l for v, l in t.uvsDict.items() if l}
        elif t.isUnicode():
            t.cmap = {
                u: g
                for u, g in t.cmap.items()
                if g in s.glyphs_requested or u in s.unicodes_requested
            }
            # Collect format 12 tables that hold only basic multilingual plane
            # codepoints.
            if t.format == 12 and t.cmap and max(t.cmap.keys()) < 0x10000:
                tables_format12_bmp.append(t)
        else:
            t.cmap = {u: g for u, g in t.cmap.items() if g in s.glyphs_requested}

    # Fomat 12 tables are redundant if they contain just the same BMP codepoints
    # their little BMP-only encoding siblings contain.
    for t in tables_format12_bmp:
        if (
            t.platformID == 0  # Unicode platform
            and t.platEncID == 4  # Unicode full repertoire
            and t.language in table_plat0_enc3  # Have a BMP-only sibling?
            and table_plat0_enc3[t.language].cmap == t.cmap
        ):
            t.cmap.clear()
        elif (
            t.platformID == 3  # Windows platform
            and t.platEncID == 10  # Unicode full repertoire
            and t.language in table_plat3_enc1  # Have a BMP-only sibling?
            and table_plat3_enc1[t.language].cmap == t.cmap
        ):
            t.cmap.clear()

    self.tables = [t for t in self.tables if (t.cmap if t.format != 14 else t.uvsDict)]
    self.numSubTables = len(self.tables)
    # TODO(behdad) Convert formats when needed.
    # In particular, if we have a format=12 without non-BMP
    # characters, convert it to format=4 if there's not one.
    return True  # Required table

