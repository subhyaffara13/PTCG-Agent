
def is_tensor_list(typ: Type) -> bool:
    return isinstance(typ, ListType) and is_tensor(typ.elem)

