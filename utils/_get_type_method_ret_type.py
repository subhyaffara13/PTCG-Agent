
def _get_type_method_ret_type(t: ProperType, *, name: str) -> Type | None:
    # For Enum literals the ret_type can change based on the Enum
    # we need to check the type of the enum rather than the literal
    if isinstance(t, LiteralType) and t.is_enum_literal():
        t = t.fallback

    if isinstance(t, Instance):
        sym = t.type.get(name)
        if sym:
            sym_type = get_proper_type(sym.type)
            if isinstance(sym_type, CallableType):
                return sym_type.ret_type

    return None

