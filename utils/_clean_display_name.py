
def _clean_display_name(raw: str) -> str:
    return _SLUG_SUFFIX_RE.sub("", raw).strip()

