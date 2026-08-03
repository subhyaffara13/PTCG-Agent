from typing import Any

def _getmp(self: JpegImageFile) -> dict[int, Any] | None:
    # Extract MP information.  This method was inspired by the "highly
    # experimental" _getexif version that's been in use for years now,
    # itself based on the ImageFileDirectory class in the TIFF plugin.

    # The MP record essentially consists of a TIFF file embedded in a JPEG
    # application marker.
    try:
        data = self.info["mp"]
    except KeyError:
        return None
    file_contents = io.BytesIO(data)
    head = file_contents.read(8)
    endianness = ">" if head.startswith(b"\x4d\x4d\x00\x2a") else "<"
    # process dictionary
    from . import TiffImagePlugin

    try:
        info = TiffImagePlugin.ImageFileDirectory_v2(head)
        file_contents.seek(info.next)
        info.load(file_contents)
        mp = dict(info)
    except Exception as e:
        msg = "malformed MP Index (unreadable directory)"
        raise SyntaxError(msg) from e
    # it's an error not to have a number of images
    try:
        quant = mp[0xB001]
    except KeyError as e:
        msg = "malformed MP Index (no number of images)"
        raise SyntaxError(msg) from e
    # get MP entries
    mpentries = []
    try:
        rawmpentries = mp[0xB002]
        for entrynum in range(quant):
            unpackedentry = struct.unpack_from(
                f"{endianness}LLLHH", rawmpentries, entrynum * 16
            )
            labels = ("Attribute", "Size", "DataOffset", "EntryNo1", "EntryNo2")
            mpentry = dict(zip(labels, unpackedentry))
            mpentryattr = {
                "DependentParentImageFlag": bool(mpentry["Attribute"] & (1 << 31)),
                "DependentChildImageFlag": bool(mpentry["Attribute"] & (1 << 30)),
                "RepresentativeImageFlag": bool(mpentry["Attribute"] & (1 << 29)),
                "Reserved": (mpentry["Attribute"] & (3 << 27)) >> 27,
                "ImageDataFormat": (mpentry["Attribute"] & (7 << 24)) >> 24,
                "MPType": mpentry["Attribute"] & 0x00FFFFFF,
            }
            if mpentryattr["ImageDataFormat"] == 0:
                mpentryattr["ImageDataFormat"] = "JPEG"
            else:
                msg = "unsupported picture format in MPO"
                raise SyntaxError(msg)
            mptypemap = {
                0x000000: "Undefined",
                0x010001: "Large Thumbnail (VGA Equivalent)",
                0x010002: "Large Thumbnail (Full HD Equivalent)",
                0x020001: "Multi-Frame Image (Panorama)",
                0x020002: "Multi-Frame Image: (Disparity)",
                0x020003: "Multi-Frame Image: (Multi-Angle)",
                0x030000: "Baseline MP Primary Image",
            }
            mpentryattr["MPType"] = mptypemap.get(mpentryattr["MPType"], "Unknown")
            mpentry["Attribute"] = mpentryattr
            mpentries.append(mpentry)
        mp[0xB002] = mpentries
    except KeyError as e:
        msg = "malformed MP Index (bad MP Entry)"
        raise SyntaxError(msg) from e
    # Next we should try and parse the individual image unique ID list;
    # we don't because I've never seen this actually used in a real MPO
    # file and so can't test it.
    return mp

