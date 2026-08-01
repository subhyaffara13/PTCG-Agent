
def _Lookup_PairPos_get_effective_value_pair(
    merger, subtables, firstGlyph, secondGlyph
):
    for self in subtables:
        if (
            self is None
            or type(self) != ot.PairPos
            or self.Coverage is None
            or firstGlyph not in self.Coverage.glyphs
        ):
            continue
        if self.Format == 1:
            ps = self.PairSet[self.Coverage.glyphs.index(firstGlyph)]
            pvr = ps.PairValueRecord
            for rec in pvr:  # TODO Speed up
                if rec.SecondGlyph == secondGlyph:
                    return rec
            continue
        elif self.Format == 2:
            klass1 = self.ClassDef1.classDefs.get(firstGlyph, 0)
            klass2 = self.ClassDef2.classDefs.get(secondGlyph, 0)
            return self.Class1Record[klass1].Class2Record[klass2]
        else:
            raise UnsupportedFormat(merger, subtable="pair positioning lookup")
    return None

