
def _yaml_escape(value: str) -> str:
    """Escape a string for safe embedding in a double-quoted YAML scalar."""
    return (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )

