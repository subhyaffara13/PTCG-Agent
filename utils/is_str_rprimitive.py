
def is_str_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return isinstance(rtype, RPrimitive) and rtype.name == "builtins.str"

