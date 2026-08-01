
def filter_invalid_unicode(text):
    """Return an empty string and True if 'text' is in invalid unicode."""
    return ("", True) if isinstance(text, bytes) else (text, False)

