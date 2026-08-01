
def has_type_vars(typ: Type) -> bool:
    """Check if a type contains any type variables (recursively)."""
    return typ.accept(HasTypeVars())

