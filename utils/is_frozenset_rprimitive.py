
def is_frozenset_rprimitive(rtype: RType) -> TypeGuard[RPrimitive]:
    return isinstance(rtype, RPrimitive) and rtype.name == "builtins.frozenset"

