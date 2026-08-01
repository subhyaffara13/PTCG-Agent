
def convert_to_t_ext_item(builder: LowLevelIRBuilder, item: Value) -> Value:
    vec_len = builder.add(GetElement(item, "len"))
    vec_items = builder.add(GetElement(item, "items"))
    temp = builder.add(SetElement(Undef(VecNestedBufItem), "len", vec_len))
    return builder.add(SetElement(temp, "items", vec_items))

