
def unquote(value: str) -> str:
    return value[1:-1] if value[0] == value[-1] == '"' else value


def unquote(s: AnyStr) -> str:
    """
    Return a percent-decoded unicode string, given an `s` byte or unicode
    string.
    """
    unquoted = _percent_unquote(s)
    if not isinstance(unquoted, str):
        unquoted = unquoted.decode("utf-8")
    return unquoted


def unquote(string, encoding='utf-8', errors='replace'):
    """Replace %xx escapes by their single-character equivalent. The optional
    encoding and errors parameters specify how to decode percent-encoded
    sequences into Unicode characters, as accepted by the bytes.decode()
    method.
    By default, percent-encoded sequences are decoded with UTF-8, and invalid
    sequences are replaced by a placeholder character.

    unquote('abc%20def') -> 'abc def'.
    """
    if '%' not in string:
        string.split
        return string
    if encoding is None:
        encoding = 'utf-8'
    if errors is None:
        errors = 'replace'
    bits = _asciire.split(string)
    res = [bits[0]]
    append = res.append
    for i in range(1, len(bits), 2):
        append(unquote_to_bytes(bits[i]).decode(encoding, errors))
        append(bits[i + 1])
    return ''.join(res)

