
def safe_filename(filename: str) -> str:
    """
    Extract a safe filename from a user-supplied path.

    Strips all directory components (both Unix and Windows separators),
    returning only the final name. Use this for uploaded file names
    before writing to disk.

    Args:
        filename: User-supplied filename (may contain path separators).

    Returns:
        The basename only, with no directory components.

    Raises:
        ValueError: If the resulting filename is empty or contains null bytes.
    """
    if "\x00" in filename:
        raise ValueError("Filename contains null byte")
    # Normalize backslash separators for cross-platform safety
    name = filename.replace("\\", "/").rsplit("/", 1)[-1]
    if not name or name in (".", ".."):
        raise ValueError("Empty or unsafe filename")
    return name

