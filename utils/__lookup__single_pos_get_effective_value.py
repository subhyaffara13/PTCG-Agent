
def _Lookup_SinglePos_get_effective_value(merger, subtables, glyph):
    for self in subtables:
        if (
            self is None
            or type(self) != ot.SinglePos
            or self.Coverage is None
            or glyph not in self.Coverage.glyphs
        ):
            continue
        if self.Format == 1:
            return self.Value
        elif self.Format == 2:
            return self.Value[self.Coverage.glyphs.index(glyph)]
        else:
            raise UnsupportedFormat(merger, subtable="single positioning lookup")
    return None

