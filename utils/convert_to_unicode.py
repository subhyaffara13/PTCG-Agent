
def convert_to_unicode(text):
    """
    Converts `text` to Unicode (if it's not already), assuming UTF-8 input.
    """

    def ensure_text(s, encoding="utf-8", errors="strict"):
        if isinstance(s, bytes):
            return s.decode(encoding, errors)
        elif isinstance(s, str):
            return s
        else:
            raise TypeError(f"not expecting type '{type(s)}'")

    return ensure_text(text, encoding="utf-8", errors="ignore")

