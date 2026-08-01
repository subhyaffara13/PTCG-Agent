
def _normalize_codec_name(codec: str) -> str:
    """Make sure the codec name is always given as defined in the BOM dict."""
    return UTF_NAME_REGEX_COMPILED.sub(r"utf-\1\2", codec).lower()

