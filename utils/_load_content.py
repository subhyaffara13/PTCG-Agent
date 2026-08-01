
def _load_content(content: str | Path | bytes) -> bytes:
    """Load the content of an entry as bytes.

    Used only for small checks (not to dump content into archive).
    """
    if isinstance(content, (str, Path)):
        return Path(content).read_bytes()
    elif isinstance(content, bytes):
        return content
    else:
        raise DDUFExportError(f"Invalid content type. Must be str, Path or bytes. Got {type(content)}.")

