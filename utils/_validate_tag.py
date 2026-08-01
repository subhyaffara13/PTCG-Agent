
def _validate_tag(tag: str):
    parts = tag.split(".")
    t = _TAGS
    for part in parts:
        if not set(part) <= set(string.ascii_lowercase + "-"):
            raise AssertionError(f"Tag contains invalid characters: {part}")
        if part in t:
            t = t[part]
        else:
            raise ValueError(f"Tag {tag} is not found in registered tags.")

