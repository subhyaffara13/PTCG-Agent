
def expand_self_type(var: Var, typ: ProperType, replacement: ProperType) -> ProperType: ...


def expand_self_type(var: Var, typ: Type, replacement: Type) -> Type: ...


def expand_self_type(var: Var, typ: Type, replacement: Type) -> Type:
    """Expand appearances of Self type in a variable type."""
    if var.info.self_type is not None and not var.is_property:
        return expand_type(typ, {var.info.self_type.id: replacement})
    return typ

