
def filter_language(text):
    """Remove inappropriate/violent language."""
    return _CENSOR_PATTERN.sub(replacer, text)

