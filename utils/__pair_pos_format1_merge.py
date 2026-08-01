
def _PairPosFormat1_merge(self, lst, merger):
    assert allEqual(
        [l.ValueFormat2 == 0 for l in lst if l.PairSet]
    ), "Report bug against fonttools."

    # Merge everything else; makes sure Format is the same.
    merger.mergeObjects(
        self,
        lst,
        exclude=("Coverage", "PairSet", "PairSetCount", "ValueFormat1", "ValueFormat2"),
    )

    empty = ot.PairSet()
    empty.PairValueRecord = []
    empty.PairValueCount = 0

    # Align them
    glyphs, padded = _merge_GlyphOrders(
        merger.font,
        [v.Coverage.glyphs for v in lst],
        [v.PairSet for v in lst],
        default=empty,
    )

    self.Coverage.glyphs = glyphs
    self.PairSet = [ot.PairSet() for _ in glyphs]
    self.PairSetCount = len(self.PairSet)
    for glyph, ps in zip(glyphs, self.PairSet):
        ps._firstGlyph = glyph

    merger.mergeLists(self.PairSet, padded)

