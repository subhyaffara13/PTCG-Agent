
def _Lookup_PairPosFormat1_subtables_flatten(lst, font):
    assert allEqual(
        [l.ValueFormat2 == 0 for l in lst if l.PairSet]
    ), "Report bug against fonttools."

    self = ot.PairPos()
    self.Format = 1
    self.Coverage = ot.Coverage()
    self.ValueFormat1 = reduce(int.__or__, [l.ValueFormat1 for l in lst], 0)
    self.ValueFormat2 = reduce(int.__or__, [l.ValueFormat2 for l in lst], 0)

    # Align them
    glyphs, padded = _merge_GlyphOrders(
        font, [v.Coverage.glyphs for v in lst], [v.PairSet for v in lst]
    )

    self.Coverage.glyphs = glyphs
    self.PairSet = [
        _PairSet_flatten([v for v in values if v is not None], font)
        for values in zip(*padded)
    ]
    self.PairSetCount = len(self.PairSet)
    return self

