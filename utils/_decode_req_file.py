
def _decode_req_file(data: bytes, url: str) -> str:
    for bom, encoding in BOMS:
        if data.startswith(bom):
            return data[len(bom) :].decode(encoding)

    for line in data.split(b"\n")[:2]:
        if line[0:1] == b"#":
            result = PEP263_ENCODING_RE.search(line)
            if result is not None:
                encoding = result.groups()[0].decode("ascii")
                return data.decode(encoding)

    try:
        return data.decode(DEFAULT_ENCODING)
    except UnicodeDecodeError:
        locale_encoding = locale.getpreferredencoding(False) or sys.getdefaultencoding()
        logging.warning(
            "unable to decode data from %s with default encoding %s, "
            "falling back to encoding from locale: %s. "
            "If this is intentional you should specify the encoding with a "
            "PEP-263 style comment, e.g. '# -*- coding: %s -*-'",
            url,
            DEFAULT_ENCODING,
            locale_encoding,
            locale_encoding,
        )
        return data.decode(locale_encoding)

