
def _apply_gemini_mime_type_aliases(mime_type: str) -> str:
    """Normalize known MIME aliases only; does not consult the file-type registry.

    Also strips MIME parameters (e.g. ``; charset=utf-8``) so that values
    sourced from GCS object metadata (``contentType``) validate correctly.
    """
    normalized = mime_type.split(";", 1)[0].strip().lower()
    return _GEMINI_MIME_TYPE_ALIASES.get(normalized, normalized)

