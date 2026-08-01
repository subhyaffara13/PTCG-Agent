
def _line_length(line: _StrLike, codec: str) -> int:
    """Get the length of a string like line as displayed in an editor."""
    if isinstance(line, bytes):
        decoded = _remove_bom(line, codec).decode(codec, "replace")
    else:
        decoded = line

    stripped = decoded.rstrip("\n")

    if stripped != decoded:
        stripped = stripped.rstrip("\r")

    return len(stripped)

