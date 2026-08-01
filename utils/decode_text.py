
def decode_text(b: bytes) -> str:
    if b[: len(codecs.BOM_UTF16_BE)] == codecs.BOM_UTF16_BE:
        return b[len(codecs.BOM_UTF16_BE) :].decode("utf_16_be")
    else:
        return "".join(PDFDocEncoding.get(byte, chr(byte)) for byte in b)

