
def vec_item_type(builder: LowLevelIRBuilder, item_type: RType, line: int) -> Value:
    typeobj, optional, depth = vec_item_type_info(builder, item_type, line)
    assert typeobj is not None
    if isinstance(typeobj, Integer):
        return typeobj
    else:
        # Create an integer which will hold the type object * as an integral value.
        # Assign implicitly coerces between pointer/integer types.
        typeval: Value
        typeval = Register(pointer_rprimitive)
        builder.add(Assign(typeval, typeobj))
        if optional:
            typeval = builder.add(
                IntOp(pointer_rprimitive, typeval, Integer(1, pointer_rprimitive), IntOp.OR)
            )
        return typeval

