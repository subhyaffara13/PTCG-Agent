import re

def _compile_pattern(pattern: str) -> re.Pattern | None:
    """
    Compile a regex pattern and cache it. Returns None if pattern is invalid.

    Args:
        pattern: The regex pattern string to compile

    Returns:
        Compiled regex pattern or None if invalid
    """
    if pattern in _compiled_patterns_cache:
        return _compiled_patterns_cache[pattern]

    try:
        compiled = re.compile(pattern)
        _compiled_patterns_cache[pattern] = compiled
        return compiled
    except re.error as e:
        logger.warning(f"Invalid regex pattern '{pattern}': {e}. Treating as non-pattern.")
        return None

