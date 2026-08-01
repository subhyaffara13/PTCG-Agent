
def _gen_default_accept_encoding() -> str:
    encodings = [
        "gzip",
        "deflate",
    ]
    if HAS_BROTLI:
        encodings.append("br")
    if HAS_ZSTD:
        encodings.append("zstd")
    return ", ".join(encodings)

