
def writeTTCHeader(file, numFonts):
    self = SimpleNamespace()
    self.TTCTag = "ttcf"
    self.Version = 0x00010000
    self.numFonts = numFonts
    file.seek(0)
    file.write(sstruct.pack(ttcHeaderFormat, self))
    offset = file.tell()
    file.write(struct.pack(">%dL" % self.numFonts, *([0] * self.numFonts)))
    return offset

