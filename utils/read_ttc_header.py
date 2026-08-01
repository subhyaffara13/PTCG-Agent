
def readTTCHeader(file):
    file.seek(0)
    data = file.read(ttcHeaderSize)
    if len(data) != ttcHeaderSize:
        raise TTLibError("Not a Font Collection (not enough data)")
    self = SimpleNamespace()
    sstruct.unpack(ttcHeaderFormat, data, self)
    if self.TTCTag != "ttcf":
        raise TTLibError("Not a Font Collection")
    assert self.Version == 0x00010000 or self.Version == 0x00020000, (
        "unrecognized TTC version 0x%08x" % self.Version
    )
    self.offsetTable = struct.unpack(
        ">%dL" % self.numFonts, file.read(self.numFonts * 4)
    )
    if self.Version == 0x00020000:
        pass  # ignoring version 2.0 signatures
    return self

