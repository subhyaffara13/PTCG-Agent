
def has_bool_item(typ: ProperType) -> bool:
    """Return True if type is 'bool' or a union with a 'bool' item."""
    if is_named_instance(typ, "builtins.bool"):
        return True
    if isinstance(typ, UnionType):
        return any(is_named_instance(item, "builtins.bool") for item in typ.items)
    return False

