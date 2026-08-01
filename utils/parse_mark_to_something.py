
def parseMarkToSomething(lines, font, c):
    self = c.Type()
    self.Format = 1
    markData = {}
    baseData = {}
    Data = {
        "mark": (markData, c.MarkAnchorClass),
        "base": (baseData, c.BaseAnchorClass),
        "ligature": (baseData, c.BaseAnchorClass),
    }
    maxKlass = 0
    for line in lines:
        typ = line[0]
        assert typ in ("mark", "base", "ligature")
        glyph = makeGlyph(line[1])
        data, anchorClass = Data[typ]
        extraItems = 2 if typ == "ligature" else 0
        extras = tuple(int(i) for i in line[2 : 2 + extraItems])
        klass = int(line[2 + extraItems])
        anchor = makeAnchor(line[3 + extraItems :], anchorClass)
        if typ == "mark":
            key, value = glyph, (klass, anchor)
        else:
            key, value = ((glyph, klass) + extras), anchor
        assert key not in data, key
        data[key] = value
        maxKlass = max(maxKlass, klass)

    # Mark
    markCoverage = makeCoverage(set(markData.keys()), font, c.MarkCoverageClass)
    markArray = c.MarkArrayClass()
    markRecords = makeMarkRecords(markData, markCoverage, c)
    setattr(markArray, c.MarkRecord, markRecords)
    setattr(markArray, c.MarkCount, len(markRecords))
    setattr(self, c.MarkCoverage, markCoverage)
    setattr(self, c.MarkArray, markArray)
    self.ClassCount = maxKlass + 1

    # Base
    self.classCount = 0 if not baseData else 1 + max(k[1] for k, v in baseData.items())
    baseCoverage = makeCoverage(
        set([k[0] for k in baseData.keys()]), font, c.BaseCoverageClass
    )
    baseArray = c.BaseArrayClass()
    if c.Base == "Ligature":
        baseRecords = makeLigatureRecords(baseData, baseCoverage, c, self.classCount)
    else:
        baseRecords = makeBaseRecords(baseData, baseCoverage, c, self.classCount)
    setattr(baseArray, c.BaseRecord, baseRecords)
    setattr(baseArray, c.BaseCount, len(baseRecords))
    setattr(self, c.BaseCoverage, baseCoverage)
    setattr(self, c.BaseArray, baseArray)

    return self

