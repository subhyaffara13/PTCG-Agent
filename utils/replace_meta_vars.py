
def replace_meta_vars(t: Type, target_type: Type) -> Type:
    """Replace unification variables in a type with the target type."""
    return t.accept(TypeVarEraser(erase_meta_id, target_type))

