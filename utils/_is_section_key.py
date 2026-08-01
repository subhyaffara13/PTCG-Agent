
def _is_section_key(key: str) -> bool:
    """Is a Config key a section name (does it start with a capital)?"""
    return bool(key and key[0].upper() == key[0] and not key.startswith("_"))

