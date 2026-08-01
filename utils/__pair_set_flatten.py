
def _PairSet_flatten(lst, font):
    self = ot.PairSet()
    self.Coverage = ot.Coverage()

    # Align them
    glyphs, padded = _merge_GlyphOrders(
        font,
        [[v.SecondGlyph for v in vs.PairValueRecord] for vs in lst],
        [vs.PairValueRecord for vs in lst],
    )

    self.Coverage.glyphs = glyphs
    self.PairValueRecord = pvrs = []
    for values in zip(*padded):
        for v in values:
            if v is not None:
                pvrs.append(v)
                break
        else:
            assert False
    self.PairValueCount = len(self.PairValueRecord)

    return self

