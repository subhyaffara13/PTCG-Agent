
def delete_nested_value(
    data: Dict[str, Any],
    path: str,
    depth: int = 0,
    max_depth: int = 20,
) -> Dict[str, Any]:
    """
    Delete a field from nested data using JSONPath notation.

    Custom implementation - no external dependencies.

    Supports:
    - "field" - top-level field
    - "parent.child" - nested field
    - "array[*]" - all array elements (wildcard)
    - "array[0]" - specific array element (index)
    - "array[*].field" - field in all array elements

    Args:
        data: Dictionary to modify (creates deep copy)
        path: JSONPath-like path string
        depth: Current recursion depth (kept for API compatibility)
        max_depth: Maximum recursion depth (kept for API compatibility)

    Returns:
        New dictionary with field removed at path

    Example:
        >>> data = {"tools": [{"name": "t1", "input_examples": ["ex"]}]}
        >>> delete_nested_value(data, "tools[*].input_examples")
        {"tools": [{"name": "t1"}]}
    """
    import copy

    result = copy.deepcopy(data)

    try:
        # Parse path into segments
        segments = _parse_path_segments(path)

        if not segments:
            return result

        # Delete using custom recursive implementation
        _delete_nested_value_custom(result, segments, 0)

    except Exception:
        # Invalid path or parsing error - silently skip
        pass

    return result

