
def defined_in_superclass(info: TypeInfo, name: str) -> bool:
    """Check if a variable has an explicit value at class level in any of superclasses."""
    for base in info.mro[1:]:
        if (node := base.names.get(name)) is not None:
            if not node.implicit and isinstance(node.node, Var) and node.node.has_explicit_value:
                return True
    return False

