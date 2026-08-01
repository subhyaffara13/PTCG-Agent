
def _normalize_mime(value: str) -> list[str]:
    return _mime_split_re.split(value.lower())

