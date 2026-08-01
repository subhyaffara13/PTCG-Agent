
def _normalize_lang(value: str) -> list[str]:
    """Process a language tag for matching."""
    return _locale_delim_re.split(value.lower())

