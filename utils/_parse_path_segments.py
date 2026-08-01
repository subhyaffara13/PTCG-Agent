
def _parse_path_segments(path: str) -> list:
    """
    Parse a JSONPath-like string into segments using regex.

    Handles:
    - Dot notation: "a.b.c" → ["a", "b", "c"]
    - Array wildcards: "a[*].b" → ["a", "[*]", "b"]
    - Array indices: "a[0].b" → ["a", "[0]", "b"]

    Args:
        path: JSONPath-like path string

    Returns:
        List of path segments

    Example:
        >>> _parse_path_segments("tools[*].arr[0].field")
        ["tools", "[*]", "arr", "[0]", "field"]
    """
    import re

    # Match field names OR bracket expressions
    # Pattern: field_name (anything except . or [) | [anything_in_brackets]
    pattern = r"[^\.\[]+|\[[^\]]*\]"
    segments = re.findall(pattern, path)
    return segments

