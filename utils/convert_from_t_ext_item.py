
def convert_from_t_ext_item(builder: LowLevelIRBuilder, item: Value, vec_type: RVec) -> Value:
    """Convert an owned VecNestedBufItem to the corresponding RVec value."""
    vec_len = builder.add(GetElement(item, "len"))
    vec_items = builder.add(GetElement(item, "items"))
    temp = builder.add(SetElement(Undef(vec_type), "len", vec_len))
    return builder.add(SetElement(temp, "items", vec_items))

