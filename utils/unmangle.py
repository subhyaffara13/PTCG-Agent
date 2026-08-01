
def unmangle(name: str) -> str:
    """Remove internal suffixes from a short name."""
    return name.rstrip("'")

