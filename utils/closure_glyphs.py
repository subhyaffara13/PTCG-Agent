
def closure_glyphs(self, s):
    cff = self.cff
    assert len(cff) == 1
    font = cff[cff.keys()[0]]
    glyphSet = font.CharStrings

    decompose = s.glyphs
    while decompose:
        components = set()
        for g in decompose:
            if g not in glyphSet:
                continue
            gl = glyphSet[g]

            subrs = getattr(gl.private, "Subrs", [])
            decompiler = _ClosureGlyphsT2Decompiler(components, subrs, gl.globalSubrs)
            decompiler.execute(gl)
        components -= s.glyphs
        s.glyphs.update(components)
        decompose = components


def closure_glyphs(self, s, cur_glyphs):
    s.glyphs.update(v for g, v in self.mapping.items() if g in cur_glyphs)


def closure_glyphs(self, s, cur_glyphs):
    for glyph, subst in self.mapping.items():
        if glyph in cur_glyphs:
            s.glyphs.update(subst)


def closure_glyphs(self, s, cur_glyphs):
    s.glyphs.update(*(vlist for g, vlist in self.alternates.items() if g in cur_glyphs))


def closure_glyphs(self, s, cur_glyphs):
    s.glyphs.update(
        *(
            [seq.LigGlyph for seq in seqs if all(c in s.glyphs for c in seq.Component)]
            for g, seqs in self.ligatures.items()
            if g in cur_glyphs
        )
    )


def closure_glyphs(self, s, cur_glyphs):
    if self.Format == 1:
        indices = self.Coverage.intersect(cur_glyphs)
        if not indices or not all(
            c.intersect(s.glyphs)
            for c in self.LookAheadCoverage + self.BacktrackCoverage
        ):
            return
        s.glyphs.update(self.Substitute[i] for i in indices)
    else:
        assert 0, "unknown format: %s" % self.Format


def closure_glyphs(self, s, cur_glyphs):
    c = self.__subset_classify_context()

    indices = c.Coverage(self).intersect(cur_glyphs)
    if not indices:
        return []
    cur_glyphs = c.Coverage(self).intersect_glyphs(cur_glyphs)

    if self.Format == 1:
        ContextData = c.ContextData(self)
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        for i in indices:
            if i >= rssCount or not rss[i]:
                continue
            for r in getattr(rss[i], c.Rule):
                if not r:
                    continue
                if not all(
                    all(c.Intersect(s.glyphs, cd, k) for k in klist)
                    for cd, klist in zip(ContextData, c.RuleData(r))
                ):
                    continue
                chaos = set()
                for ll in getattr(r, c.LookupRecord):
                    if not ll:
                        continue
                    seqi = ll.SequenceIndex
                    if seqi in chaos:
                        # TODO Can we improve this?
                        pos_glyphs = None
                    else:
                        if seqi == 0:
                            pos_glyphs = frozenset([c.Coverage(self).glyphs[i]])
                        else:
                            pos_glyphs = frozenset([r.Input[seqi - 1]])
                    lookup = s.table.LookupList.Lookup[ll.LookupListIndex]
                    chaos.add(seqi)
                    if lookup.may_have_non_1to1():
                        chaos.update(range(seqi, len(r.Input) + 2))
                    lookup.closure_glyphs(s, cur_glyphs=pos_glyphs)
    elif self.Format == 2:
        ClassDef = getattr(self, c.ClassDef)
        indices = ClassDef.intersect(cur_glyphs)
        ContextData = c.ContextData(self)
        rss = getattr(self, c.RuleSet)
        rssCount = getattr(self, c.RuleSetCount)
        for i in indices:
            if i >= rssCount or not rss[i]:
                continue
            for r in getattr(rss[i], c.Rule):
                if not r:
                    continue
                if not all(
                    all(c.Intersect(s.glyphs, cd, k) for k in klist)
                    for cd, klist in zip(ContextData, c.RuleData(r))
                ):
                    continue
                chaos = set()
                for ll in getattr(r, c.LookupRecord):
                    if not ll:
                        continue
                    seqi = ll.SequenceIndex
                    if seqi in chaos:
                        # TODO Can we improve this?
                        pos_glyphs = None
                    else:
                        if seqi == 0:
                            pos_glyphs = frozenset(
                                ClassDef.intersect_class(cur_glyphs, i)
                            )
                        else:
                            pos_glyphs = frozenset(
                                ClassDef.intersect_class(
                                    s.glyphs, getattr(r, c.Input)[seqi - 1]
                                )
                            )
                    lookup = s.table.LookupList.Lookup[ll.LookupListIndex]
                    chaos.add(seqi)
                    if lookup.may_have_non_1to1():
                        chaos.update(range(seqi, len(getattr(r, c.Input)) + 2))
                    lookup.closure_glyphs(s, cur_glyphs=pos_glyphs)
    elif self.Format == 3:
        if not all(x is not None and x.intersect(s.glyphs) for x in c.RuleData(self)):
            return []
        r = self
        input_coverages = getattr(r, c.Input)
        chaos = set()
        for ll in getattr(r, c.LookupRecord):
            if not ll:
                continue
            seqi = ll.SequenceIndex
            if seqi in chaos:
                # TODO Can we improve this?
                pos_glyphs = None
            else:
                if seqi == 0:
                    pos_glyphs = frozenset(cur_glyphs)
                else:
                    pos_glyphs = frozenset(
                        input_coverages[seqi].intersect_glyphs(s.glyphs)
                    )
            lookup = s.table.LookupList.Lookup[ll.LookupListIndex]
            chaos.add(seqi)
            if lookup.may_have_non_1to1():
                chaos.update(range(seqi, len(input_coverages) + 1))
            lookup.closure_glyphs(s, cur_glyphs=pos_glyphs)
    else:
        assert 0, "unknown format: %s" % self.Format


def closure_glyphs(self, s, cur_glyphs):
    if self.Format == 1:
        self.ExtSubTable.closure_glyphs(s, cur_glyphs)
    else:
        assert 0, "unknown format: %s" % self.Format


def closure_glyphs(self, s, cur_glyphs=None):
    if cur_glyphs is None:
        cur_glyphs = frozenset(s.glyphs)

    # Memoize
    key = id(self)
    doneLookups = s._doneLookups
    count, covered = doneLookups.get(key, (0, None))
    if count != len(s.glyphs):
        count, covered = doneLookups[key] = (len(s.glyphs), set())
    if cur_glyphs.issubset(covered):
        return
    covered.update(cur_glyphs)

    for st in self.SubTable:
        if not st:
            continue
        st.closure_glyphs(s, cur_glyphs)


def closure_glyphs(self, s):
    s.table = self.table
    if self.table.ScriptList:
        feature_indices = self.table.ScriptList.collect_features()
    else:
        feature_indices = []
    if self.table.FeatureList:
        lookup_indices = self.table.FeatureList.collect_lookups(feature_indices)
    else:
        lookup_indices = []
    if getattr(self.table, "FeatureVariations", None):
        lookup_indices += self.table.FeatureVariations.collect_lookups(feature_indices)
    lookup_indices = _uniq_sort(lookup_indices)
    if self.table.LookupList:
        s._doneLookups = {}
        while True:
            orig_glyphs = frozenset(s.glyphs)
            for i in lookup_indices:
                if i >= self.table.LookupList.LookupCount:
                    continue
                if not self.table.LookupList.Lookup[i]:
                    continue
                self.table.LookupList.Lookup[i].closure_glyphs(s)
            if orig_glyphs == s.glyphs:
                break
        del s._doneLookups
    del s.table


def closure_glyphs(self, s):
    table = self.table.Baseline
    if table.Format in (2, 3):
        s.glyphs.add(table.StandardGlyph)


def closure_glyphs(self, s):
    if self.version > 0:
        # on decompiling COLRv1, we only keep around the raw otTables
        # but for subsetting we need dicts with fully decompiled layers;
        # we store them temporarily in the C_O_L_R_ instance and delete
        # them after we have finished subsetting.
        self.ColorLayers = self._decompileColorLayersV0(self.table)
        self.ColorLayersV1 = {
            rec.BaseGlyph: rec.Paint
            for rec in self.table.BaseGlyphList.BaseGlyphPaintRecord
        }

    decompose = s.glyphs
    while decompose:
        layers = set()
        for g in decompose:
            for layer in self.ColorLayers.get(g, []):
                layers.add(layer.name)

            if self.version > 0:
                paint = self.ColorLayersV1.get(g)
                if paint is not None:
                    layers.update(_paint_glyph_names(paint, self.table))

        layers -= s.glyphs
        s.glyphs.update(layers)
        decompose = layers


def closure_glyphs(self, glyphs):
    variants = set()
    for v in self.MathGlyphVariantRecord:
        variants.add(v.VariantGlyph)
    if self.GlyphAssembly:
        for p in self.GlyphAssembly.PartRecords:
            variants.add(p.glyph)
    return variants


def closure_glyphs(self, s):
    glyphs = frozenset(s.glyphs)
    variants = set()

    if self.VertGlyphCoverage:
        indices = self.VertGlyphCoverage.intersect(glyphs)
        for i in indices:
            variants.update(self.VertGlyphConstruction[i].closure_glyphs(glyphs))

    if self.HorizGlyphCoverage:
        indices = self.HorizGlyphCoverage.intersect(glyphs)
        for i in indices:
            variants.update(self.HorizGlyphConstruction[i].closure_glyphs(glyphs))

    s.glyphs.update(variants)


def closure_glyphs(self, s):
    if self.table.VarCompositeGlyphs is None:
        return

    glyphMap = {glyphName: i for i, glyphName in enumerate(self.table.Coverage.glyphs)}
    glyphRecords = self.table.VarCompositeGlyphs.VarCompositeGlyph

    glyphs = s.glyphs
    covered = set()
    new = set(glyphs)
    while new:
        oldNew = new
        new = set()
        for glyphName in oldNew:
            if glyphName in covered:
                continue
            idx = glyphMap.get(glyphName)
            if idx is None:
                continue
            glyph = glyphRecords[idx]
            for comp in glyph.components:
                name = comp.glyphName
                glyphs.add(name)
                if name not in covered:
                    new.add(name)


def closure_glyphs(self, s):
    if self.table.MathVariants:
        self.table.MathVariants.closure_glyphs(s)


def closure_glyphs(self, s):
    glyphSet = self.glyphs
    decompose = s.glyphs
    while decompose:
        components = set()
        for g in decompose:
            if g not in glyphSet:
                continue
            gl = glyphSet[g]
            for c in gl.getComponentNames(self):
                components.add(c)
        components -= s.glyphs
        s.glyphs.update(components)
        decompose = components


def closure_glyphs(self, s):
    tables = [t for t in self.tables if t.isUnicode()]

    # Closure unicodes, which for now is pulling in bidi mirrored variants
    if s.options.bidi_closure:
        additional_unicodes = set()
        for u in s.unicodes_requested:
            mirror_u = mirrored(u)
            if mirror_u is not None:
                additional_unicodes.add(mirror_u)
        s.unicodes_requested.update(additional_unicodes)

    # Close glyphs
    for table in tables:
        if table.format == 14:
            for varSelector, cmap in table.uvsDict.items():
                if varSelector not in s.unicodes_requested:
                    continue
                glyphs = {g for u, g in cmap if u in s.unicodes_requested}
                if None in glyphs:
                    glyphs.remove(None)
                s.glyphs.update(glyphs)
        else:
            cmap = table.cmap
            intersection = s.unicodes_requested.intersection(cmap.keys())
            s.glyphs.update(cmap[u] for u in intersection)

    # Calculate unicodes_missing
    s.unicodes_missing = s.unicodes_requested.copy()
    for table in tables:
        s.unicodes_missing.difference_update(table.cmap)

