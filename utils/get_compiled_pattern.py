
def get_compiled_pattern(pattern_name: str) -> Pattern:
    """
    Get a compiled regex pattern by name.

    Args:
        pattern_name: Name of the prebuilt pattern

    Returns:
        Compiled regex pattern

    Raises:
        ValueError: If pattern_name is not found in PREBUILT_PATTERNS
    """
    if pattern_name not in PREBUILT_PATTERNS:
        available_patterns = ", ".join(PREBUILT_PATTERNS.keys())
        raise ValueError(
            f"Unknown pattern name: '{pattern_name}'. "
            f"Available patterns: {available_patterns}"
        )

    return re.compile(PREBUILT_PATTERNS[pattern_name], re.IGNORECASE)

