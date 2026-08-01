
def _is_file_reference(s: str) -> bool:
    """Check if string is a Gemini file reference (files/...)."""
    return isinstance(s, str) and s.startswith("files/")

