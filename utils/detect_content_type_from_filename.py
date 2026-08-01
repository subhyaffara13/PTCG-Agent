
def detect_content_type_from_filename(filename: str) -> str:
    """
    Detect content type from filename using extension.

    Uses Python's mimetypes module with custom overrides for common cases.
    Normalizes jpg to jpeg for consistency.
    """
    if not filename:
        return "application/octet-stream"

    # Try custom mapping first
    filename_lower = filename.lower()
    for ext, mime_type in EXTENSION_TO_MIME_TYPE.items():
        if filename_lower.endswith(ext):
            return mime_type

    # Fall back to Python's mimetypes
    mime_type_guess, _ = mimetypes.guess_type(filename)
    if mime_type_guess is not None:
        return mime_type_guess

    return "application/octet-stream"

