
def is_uninhabited(typ: Type) -> bool:
    return isinstance(get_proper_type(typ), UninhabitedType)

