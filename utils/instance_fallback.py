
def instance_fallback(typ: ProperType) -> Instance:
    if isinstance(typ, Instance):
        return typ
    if isinstance(typ, TupleType):
        return tuple_fallback(typ)
    if isinstance(typ, (LiteralType, TypedDictType)):
        return typ.fallback
    if instance_cache.object_type is None:
        object_typeinfo = lookup_stdlib_typeinfo("builtins.object", modules_state.modules)
        instance_cache.object_type = Instance(object_typeinfo, [])
    return instance_cache.object_type

