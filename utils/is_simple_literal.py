
def is_simple_literal(t: ProperType) -> bool:
    if isinstance(t, LiteralType):
        return t.fallback.type.is_enum or t.fallback.type.fullname == "builtins.str"
    if isinstance(t, Instance):
        return t.last_known_value is not None and isinstance(t.last_known_value.value, str)
    return False

