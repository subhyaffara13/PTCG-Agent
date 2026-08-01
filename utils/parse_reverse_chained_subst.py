
def parseReverseChainedSubst(lines, font, _lookupMap=None):
    self = ot.ReverseChainSingleSubst()
    self.Format = 1
    coverages = ([], [])
    while lines.peeks()[0].endswith("coverage definition begin"):
        typ = lines.peek()[0][: -len("coverage definition begin")].lower()
        idx, klass = {
            "backtrack": (0, ot.BacktrackCoverage),
            "lookahead": (1, ot.LookAheadCoverage),
        }[typ]
        coverages[idx].append(parseCoverage(lines, font, klass=klass))
    self.BacktrackCoverage = coverages[0]
    self.BacktrackGlyphCount = len(self.BacktrackCoverage)
    self.LookAheadCoverage = coverages[1]
    self.LookAheadGlyphCount = len(self.LookAheadCoverage)
    mapping = {}
    for line in lines:
        assert len(line) == 2, line
        line = makeGlyphs(line)
        mapping[line[0]] = line[1]
    self.Coverage = makeCoverage(set(mapping.keys()), font)
    self.Substitute = [mapping[k] for k in self.Coverage.glyphs]
    self.GlyphCount = len(self.Substitute)
    return self

