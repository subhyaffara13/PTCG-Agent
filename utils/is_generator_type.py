
def isGeneratorType(typ: Type) -> bool:
    if isinstance(typ, BaseType):
        return typ.name == BaseTy.Generator
    elif isinstance(typ, (OptionalType)):
        return isGeneratorType(typ.elem)
    return False

