
def _normalize_line_endings(source):
    source = source.replace(b"\r\n", b"\n")
    source = source.replace(b"\r", b"\n")
    return source

