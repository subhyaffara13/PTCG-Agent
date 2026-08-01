
def parseContext(lines, font, Type, lookupMap=None):
    self = getattr(ot, Type)()
    typ = lines.peeks()[0].split()[0].lower()
    if typ == "glyph":
        self.Format = 1
        log.debug("Parsing %s format %s", Type, self.Format)
        c = ContextHelper(Type, self.Format)
        rules = []
        for line in lines:
            assert line[0].lower() == "glyph", line[0]
            while len(line) < 1 + c.DataLen:
                line.append("")
            seq = tuple(makeGlyphs(stripSplitComma(i)) for i in line[1 : 1 + c.DataLen])
            recs = parseLookupRecords(line[1 + c.DataLen :], c.LookupRecord, lookupMap)
            rules.append((seq, recs))

        firstGlyphs = set(seq[c.InputIdx][0] for seq, recs in rules)
        self.Coverage = makeCoverage(firstGlyphs, font)
        bucketizeRules(self, c, rules, self.Coverage.glyphs)
    elif typ.endswith("class"):
        self.Format = 2
        log.debug("Parsing %s format %s", Type, self.Format)
        c = ContextHelper(Type, self.Format)
        classDefs = [None] * c.DataLen
        while lines.peeks()[0].endswith("class definition begin"):
            typ = lines.peek()[0][: -len("class definition begin")].lower()
            idx, klass = {
                1: {
                    "": (0, ot.ClassDef),
                },
                3: {
                    "backtrack": (0, ot.BacktrackClassDef),
                    "": (1, ot.InputClassDef),
                    "lookahead": (2, ot.LookAheadClassDef),
                },
            }[c.DataLen][typ]
            assert classDefs[idx] is None, idx
            classDefs[idx] = parseClassDef(lines, font, klass=klass)
        c.SetContextData(self, classDefs)
        rules = []
        for line in lines:
            assert line[0].lower().startswith("class"), line[0]
            while len(line) < 1 + c.DataLen:
                line.append("")
            seq = tuple(intSplitComma(i) for i in line[1 : 1 + c.DataLen])
            recs = parseLookupRecords(line[1 + c.DataLen :], c.LookupRecord, lookupMap)
            rules.append((seq, recs))
        firstClasses = set(seq[c.InputIdx][0] for seq, recs in rules)
        firstGlyphs = set(
            g for g, c in classDefs[c.InputIdx].classDefs.items() if c in firstClasses
        )
        self.Coverage = makeCoverage(firstGlyphs, font)
        bucketizeRules(self, c, rules, range(max(firstClasses) + 1))
    elif typ.endswith("coverage"):
        self.Format = 3
        log.debug("Parsing %s format %s", Type, self.Format)
        c = ContextHelper(Type, self.Format)
        coverages = tuple([] for i in range(c.DataLen))
        while lines.peeks()[0].endswith("coverage definition begin"):
            typ = lines.peek()[0][: -len("coverage definition begin")].lower()
            idx, klass = {
                1: {
                    "": (0, ot.Coverage),
                },
                3: {
                    "backtrack": (0, ot.BacktrackCoverage),
                    "input": (1, ot.InputCoverage),
                    "lookahead": (2, ot.LookAheadCoverage),
                },
            }[c.DataLen][typ]
            coverages[idx].append(parseCoverage(lines, font, klass=klass))
        c.SetRuleData(self, coverages)
        lines = list(lines)
        assert len(lines) == 1
        line = lines[0]
        assert line[0].lower() == "coverage", line[0]
        recs = parseLookupRecords(line[1:], c.LookupRecord, lookupMap)
        setattr(self, c.Type + "Count", len(recs))
        setattr(self, c.LookupRecord, recs)
    else:
        assert 0, typ
    return self

