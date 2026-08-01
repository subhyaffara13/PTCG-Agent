
def _unquote_unescape(text):
    """Returns the string, and true if it was quoted."""
    if not text:
        return text, False
    quoted = False
    text = text.strip()
    if text[0] == '"':
        if len(text) == 1 or text[-1] != '"':
            raise ValueError("missing close quote")
        text = text[1:-1]
        quoted = True
    if "\\" in text:
        text = _replace_escaping(text)
    return text, quoted

