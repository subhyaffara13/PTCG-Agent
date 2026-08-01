
def COM(self: JpegImageFile, marker: int) -> None:
    #
    # Comment marker.  Store these in the APP dictionary.
    assert self.fp is not None
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)

    self.info["comment"] = s
    self.app["COM"] = s  # compatibility
    self.applist.append(("COM", s))

