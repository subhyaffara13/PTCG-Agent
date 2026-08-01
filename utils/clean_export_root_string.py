
def clean_export_root_string(text: str) -> str:
    """Generic utility to clean export_root patterns from strings."""
    result = text
    for pattern, replacement in EXPORT_ROOT_REPLACEMENTS:
        result = result.replace(pattern, replacement)
    return result

