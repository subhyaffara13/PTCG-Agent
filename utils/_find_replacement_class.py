
def _find_replacement_class(class_name: str, mapping: dict[str, type[nn.Module]]) -> type[nn.Module] | None:
    """
    Find replacement class for a given class name, checking exact matches first, then regex patterns.

    Args:
        class_name: The class name to find a replacement for
        mapping: Dictionary of patterns/names to replacement classes

    Returns:
        The replacement class if found, None otherwise
    """
    # First check for exact match (highest priority)
    if class_name in mapping:
        return mapping[class_name]

    # Then check regex patterns
    for pattern, replacement_class in mapping.items():
        # Skip if already matched as exact
        if pattern == class_name:
            continue

        # Try to compile and match as regex
        compiled_pattern = _compile_pattern(pattern)
        if compiled_pattern is not None and compiled_pattern.search(class_name):
            return replacement_class

    return None

