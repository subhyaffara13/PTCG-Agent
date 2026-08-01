
def _sanitize_id(identifier: str) -> str:
    """Reject path traversal characters and URL-encode the identifier."""
    if any(c in identifier for c in ("/", "\\", "#", "?")):
        raise ValueError(
            f"Invalid identifier {identifier!r}: contains disallowed characters"
        )
    if ".." in identifier:
        raise ValueError(f"Invalid identifier {identifier!r}: path traversal detected")
    return urllib.parse.quote(identifier, safe="")

