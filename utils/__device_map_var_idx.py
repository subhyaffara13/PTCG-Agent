
def _Device_mapVarIdx(self, mapping, done):
    """Map VarIdx in this Device table (if any) through mapping."""
    if id(self) in done:
        return
    done.add(id(self))
    if self.DeltaFormat == 0x8000:
        varIdx = mapping[(self.StartSize << 16) + self.EndSize]
        self.StartSize = varIdx >> 16
        self.EndSize = varIdx & 0xFFFF

