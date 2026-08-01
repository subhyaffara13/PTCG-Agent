
def vec_get_item_unsafe_borrow(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    base, index = args
    return vec_get_item_unsafe_lower(builder, base, index, line, can_borrow=True)

