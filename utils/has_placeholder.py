
def has_placeholder(typ: Type) -> bool:
    """Check if a type contains any placeholder types (recursively)."""
    return typ.accept(HasPlaceholders())

