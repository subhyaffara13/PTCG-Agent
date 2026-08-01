
def APP(self: JpegImageFile, marker: int) -> None:
    #
    # Application marker.  Store these in the APP dictionary.
    # Also look for well-known application markers.

    assert self.fp is not None
    n = i16(self.fp.read(2)) - 2
    s = ImageFile._safe_read(self.fp, n)

    app = f"APP{marker & 15}"

    self.app[app] = s  # compatibility
    self.applist.append((app, s))

    if marker == 0xFFE0 and s.startswith(b"JFIF"):
        # extract JFIF information
        self.info["jfif"] = version = i16(s, 5)  # version
        self.info["jfif_version"] = divmod(version, 256)
        # extract JFIF properties
        try:
            jfif_unit = s[7]
            jfif_density = i16(s, 8), i16(s, 10)
        except Exception:
            pass
        else:
            if jfif_unit == 1:
                self.info["dpi"] = jfif_density
            elif jfif_unit == 2:  # cm
                # 1 dpcm = 2.54 dpi
                self.info["dpi"] = tuple(d * 2.54 for d in jfif_density)
            self.info["jfif_unit"] = jfif_unit
            self.info["jfif_density"] = jfif_density
    elif marker == 0xFFE1 and s.startswith(b"Exif\0\0"):
        # extract EXIF information
        if "exif" in self.info:
            self.info["exif"] += s[6:]
        else:
            self.info["exif"] = s
            self._exif_offset = self.fp.tell() - n + 6
    elif marker == 0xFFE1 and s.startswith(b"http://ns.adobe.com/xap/1.0/\x00"):
        self.info["xmp"] = s.split(b"\x00", 1)[1]
    elif marker == 0xFFE2 and s.startswith(b"FPXR\0"):
        # extract FlashPix information (incomplete)
        self.info["flashpix"] = s  # FIXME: value will change
    elif marker == 0xFFE2 and s.startswith(b"ICC_PROFILE\0"):
        # Since an ICC profile can be larger than the maximum size of
        # a JPEG marker (64K), we need provisions to split it into
        # multiple markers. The format defined by the ICC specifies
        # one or more APP2 markers containing the following data:
        #   Identifying string      ASCII "ICC_PROFILE\0"  (12 bytes)
        #   Marker sequence number  1, 2, etc (1 byte)
        #   Number of markers       Total of APP2's used (1 byte)
        #   Profile data            (remainder of APP2 data)
        # Decoders should use the marker sequence numbers to
        # reassemble the profile, rather than assuming that the APP2
        # markers appear in the correct sequence.
        self.icclist.append(s)
    elif marker == 0xFFED and s.startswith(b"Photoshop 3.0\x00"):
        # parse the image resource block
        offset = 14
        photoshop = self.info.setdefault("photoshop", {})
        try:
            while s[offset : offset + 4] == b"8BIM":
                offset += 4
                # resource code
                code = i16(s, offset)
                offset += 2
                # resource name (usually empty)
                name_len = s[offset]
                # name = s[offset+1:offset+1+name_len]
                offset += 1 + name_len
                offset += offset & 1  # align
                # resource data block
                size = i32(s, offset)
                offset += 4
                data = s[offset : offset + size]
                if code == 0x03ED:  # ResolutionInfo
                    photoshop[code] = {
                        "XResolution": i32(data, 0) / 65536,
                        "DisplayedUnitsX": i16(data, 4),
                        "YResolution": i32(data, 8) / 65536,
                        "DisplayedUnitsY": i16(data, 12),
                    }
                else:
                    photoshop[code] = data
                offset += size
                offset += offset & 1  # align
        except struct.error:
            pass  # insufficient data

    elif marker == 0xFFEE and s.startswith(b"Adobe"):
        self.info["adobe"] = i16(s, 5)
        # extract Adobe custom properties
        try:
            adobe_transform = s[11]
        except IndexError:
            pass
        else:
            self.info["adobe_transform"] = adobe_transform
    elif marker == 0xFFE2 and s.startswith(b"MPF\0"):
        # extract MPO information
        self.info["mp"] = s[4:]
        # offset is current location minus buffer size
        # plus constant header size
        self.info["mpoffset"] = self.fp.tell() - n + 4

