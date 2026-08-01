
def vec_to_list(builder: LowLevelIRBuilder, vec: Value, line: int) -> Value | None:
    return _vec_to_sequence(builder, vec, line, "to_list", list_rprimitive)

