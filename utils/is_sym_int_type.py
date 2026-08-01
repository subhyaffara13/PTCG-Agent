
def isSymIntType(typ: Type) -> bool:
    return isinstance(typ, BaseType) and typ.name == BaseTy.SymInt

