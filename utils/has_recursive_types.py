
def has_recursive_types(typ: Type) -> bool:
    """Check if a type contains any recursive aliases (recursively)."""
    _has_recursive_type.reset()
    return typ.accept(_has_recursive_type)

