
def get_nested_value(
    data: Dict[str, Any], key_path: str, default: Optional[T] = None
) -> Optional[T]:
    """
    Retrieves a value from a nested dictionary using dot notation.

    Args:
        data: The dictionary to search in
        key_path: The path to the value using dot notation (e.g., "a.b.c")
        default: The default value to return if the path is not found

    Returns:
        The value at the specified path, or the default value if not found

    Example:
        >>> data = {"a": {"b": {"c": "value"}}}
        >>> get_nested_value(data, "a.b.c")
        'value'
        >>> get_nested_value(data, "a.b.d", "default")
        'default'
        >>> data = {"kubernetes.io": {"namespace": "default"}}
        >>> get_nested_value(data, "kubernetes\\.io.namespace")
        'default'
    """
    if not key_path:
        return default

    # Remove metadata. prefix if it exists
    key_path = (
        key_path.replace("metadata.", "", 1)
        if key_path.startswith("metadata.")
        else key_path
    )

    # Split the key path into parts, respecting escaped dots (\.)
    # Use a temporary placeholder, split on unescaped dots, then restore
    placeholder = "\x00"
    parts = key_path.replace("\\.", placeholder).split(".")
    parts = [p.replace(placeholder, ".") for p in parts]

    # Traverse through the dictionary
    current: Any = data
    for part in parts:
        try:
            current = current[part]
        except (KeyError, TypeError):
            return default

    # If default is None, we can return any type
    if default is None:
        return current

    # Otherwise, ensure the type matches the default
    return current if isinstance(current, type(default)) else default

