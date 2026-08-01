
def meta_has_operator(item: Type, op_method: str) -> bool:
    item = get_proper_type(item)
    if isinstance(item, AnyType):
        return True
    item = instance_fallback(item)
    meta = item.type.metaclass_type
    if meta is None:
        type_type = lookup_stdlib_typeinfo("builtins.type", modules_state.modules)
        meta = Instance(type_type, [])
    return meta.type.has_readable_member(op_method)

