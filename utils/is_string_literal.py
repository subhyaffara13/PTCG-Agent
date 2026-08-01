
def is_string_literal(typ: Type) -> bool:
    strs = try_getting_str_literals_from_type(typ)
    return strs is not None and len(strs) == 1

