
def vec_item_type_info(
    builder: LowLevelIRBuilder, typ: RType, line: int
) -> tuple[Value | None, bool, int]:
    if isinstance(typ, RPrimitive) and typ.is_refcounted:
        return builder.load_builtin(typ.name, line), False, 0
    elif isinstance(typ, RInstance):
        return builder.load_native_type_object(typ.name), False, 0
    elif typ in vec_item_type_tags:
        return Integer(vec_item_type_tags[typ], c_size_t_rprimitive), False, 0
    elif isinstance(typ, RUnion):
        non_opt = optional_value_type(typ)
        assert non_opt is not None
        typeval, _, _ = vec_item_type_info(builder, non_opt, line)
        if typeval is not None:
            return typeval, True, 0
    elif isinstance(typ, RVec):
        typeval, optional, depth = vec_item_type_info(builder, typ.item_type, line)
        if typeval is not None:
            return typeval, optional, depth + 1
    return None, False, 0

