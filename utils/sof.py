
def SOF(self: JpegImageFile, marker: int) -> None:
    #
    # Start of frame marker.  Defines the size and mode of the
    # image.  JPEG is colour blind, so we use some simple
    # heuristics to map the number of layers to an appropriate
    # mode.  Note that this could be made a bit brighter, by
    # looking for JFIF and Adobe APP markers.

    assert self.fp is not None
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)
    self._size = i16(s, 3), i16(s, 1)
    if self._im is not None and self.size != self.im.size:
        self._im = None

    self.bits = s[0]
    if self.bits != 8:
        msg = f"cannot handle {self.bits}-bit layers"
        raise SyntaxError(msg)

    self.layers = s[5]
    if self.layers == 1:
        self._mode = "L"
    elif self.layers == 3:
        self._mode = "RGB"
    elif self.layers == 4:
        self._mode = "CMYK"
    else:
        msg = f"cannot handle {self.layers}-layer images"
        raise SyntaxError(msg)

    if marker in [0xFFC2, 0xFFC6, 0xFFCA, 0xFFCE]:
        self.info["progressive"] = self.info["progression"] = 1

    if self.icclist:
        # fixup icc profile
        self.icclist.sort()  # sort by sequence number
        if self.icclist[0][13] == len(self.icclist):
            profile = [p[14:] for p in self.icclist]
            icc_profile = b"".join(profile)
        else:
            icc_profile = None  # wrong number of fragments
        self.info["icc_profile"] = icc_profile
        self.icclist = []

    for i in range(6, len(s), 3):
        t = s[i : i + 3]
        # 4-tuples: id, vsamp, hsamp, qtable
        self.layer.append((t[0], t[1] // 16, t[1] & 15, t[2]))

