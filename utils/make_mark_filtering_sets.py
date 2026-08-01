
def makeMarkFilteringSets(sets, font):
    self = ot.MarkGlyphSetsDef()
    self.MarkSetTableFormat = 1
    self.MarkSetCount = 1 + max(sets.keys())
    self.Coverage = [None] * self.MarkSetCount
    for k, v in sorted(sets.items()):
        self.Coverage[k] = makeCoverage(set(v), font)
    return self

