
def _sanitize_file_path(file_path: str) -> str:
    """Reject path traversal and URL-encode each path segment."""
    if "#" in file_path or "?" in file_path:
        raise ValueError(
            f"Invalid file path {file_path!r}: contains URL special characters"
        )
    parts = file_path.split("/")
    for part in parts:
        if part == "..":
            raise ValueError(
                f"Invalid file path {file_path!r}: path traversal detected"
            )
    return "/".join(urllib.parse.quote(part, safe="") for part in parts)

