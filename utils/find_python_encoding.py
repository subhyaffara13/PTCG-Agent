
def find_python_encoding(text: bytes) -> tuple[str, int]:
    """PEP-263 for detecting Python file encoding"""
    result = ENCODING_RE.match(text)
    if result:
        line = 2 if result.group(1) else 1
        encoding = result.group(3).decode("ascii")
        # Handle some aliases that Python is happy to accept and that are used in the wild.
        if encoding.startswith(("iso-latin-1-", "latin-1-")) or encoding == "iso-latin-1":
            encoding = "latin-1"
        return encoding, line
    else:
        default_encoding = "utf8"
        return default_encoding, -1

