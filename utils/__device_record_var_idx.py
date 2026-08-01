
def _Device_recordVarIdx(self, s):
    """Add VarIdx in this Device table (if any) to the set s."""
    if self.DeltaFormat == 0x8000:
        s.add((self.StartSize << 16) + self.EndSize)

