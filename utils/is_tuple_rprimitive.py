
def is_tuple_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return isinstance(rtype, RPrimitive) and rtype.name == "builtins.tuple"

