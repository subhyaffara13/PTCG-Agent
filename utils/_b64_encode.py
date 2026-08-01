
def _b64_encode(content: ContentT) -> str:
    """Encode a raw file (image, audio) into base64. Can be bytes, an opened file, a path or a URL."""
    raw_bytes = _open_as_mime_bytes(content)
    return base64.b64encode(raw_bytes).decode()

