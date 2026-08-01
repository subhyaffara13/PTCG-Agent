
def _accept(prefix: bytes) -> bool | str:
    if prefix[4:8] != b"ftyp":
        return False
    major_brand = prefix[8:12]
    if major_brand in (
        # coding brands
        b"avif",
        b"avis",
        # We accept files with AVIF container brands; we can't yet know if
        # the ftyp box has the correct compatible brands, but if it doesn't
        # then the plugin will raise a SyntaxError which Pillow will catch
        # before moving on to the next plugin that accepts the file.
        #
        # Also, because this file might not actually be an AVIF file, we
        # don't raise an error if AVIF support isn't properly compiled.
        b"mif1",
        b"msf1",
    ):
        if not SUPPORTED:
            return (
                "image file could not be identified because AVIF support not installed"
            )
        return True
    return False


def _accept(prefix: bytes) -> bool:
    return prefix.startswith((b"BLP1", b"BLP2"))


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"BM")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith((b"BUFR", b"ZCZC"))


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"\0\0\2\0")


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 4 and i32(prefix) == MAGIC


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"DDS ")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"%!PS") or (
        len(prefix) >= 4 and i32(prefix) == 0xC6D3D0C5
    )


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"SIMPLE")


def _accept(prefix: bytes) -> bool:
    return (
        len(prefix) >= 16
        and i16(prefix, 4) in [0xAF11, 0xAF12]
        and i16(prefix, 14) in [0, 3]  # flags
    )


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(olefile.MAGIC)


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(MAGIC)


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 8 and i32(prefix, 0) >= 20 and i32(prefix, 4) in (1, 2)


def _accept(prefix: bytes) -> bool:
    return prefix.startswith((b"GIF87a", b"GIF89a"))


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 8 and prefix.startswith(b"GRIB") and prefix[7] == 1


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"\x89HDF\r\n\x1a\n")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(MAGIC)


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(_MAGIC)


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(
        (b"\xff\x4f\xff\x51", b"\x00\x00\x00\x0cjP  \x0d\x0a\x87\x0a")
    )


def _accept(prefix: bytes) -> bool:
    # Magic number was taken from https://en.wikipedia.org/wiki/JPEG
    return prefix.startswith(b"\xff\xd8\xff")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"\x00\x00\x00\x00\x00\x00\x00\x04")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(olefile.MAGIC)


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"\x00\x00\x01\xb3")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith((b"DanM", b"LinS"))


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 2 and prefix[0] == 10 and prefix[1] in [0, 2, 3, 5]


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"\200\350\000\000")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(_MAGIC)


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 2 and prefix.startswith(b"P") and prefix[1] in b"0123456fy"


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"8BPS")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"qoif")


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 2 and i16(prefix) == 474


def _accept(prefix: bytes) -> bool:
    return len(prefix) >= 4 and i32(prefix) == 0x59A66A95


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(tuple(PREFIXES))


def _accept(prefix: bytes) -> bool | str:
    is_riff_file_format = prefix.startswith(b"RIFF")
    is_webp_file = prefix[8:12] == b"WEBP"
    is_valid_vp8_mode = prefix[12:16] in _VP8_MODES_BY_IDENTIFIER

    if is_riff_file_format and is_webp_file and is_valid_vp8_mode:
        if not SUPPORTED:
            return (
                "image file could not be identified because WEBP support not installed"
            )
        return True
    return False


def _accept(prefix: bytes) -> bool:
    return prefix.startswith((b"\xd7\xcd\xc6\x9a\x00\x00", b"\x01\x00\x00\x00"))


def _accept(prefix: bytes) -> bool:
    return prefix.lstrip().startswith(b"#define")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(b"/* XPM */")


def _accept(prefix: bytes) -> bool:
    return prefix.startswith(_MAGIC)

