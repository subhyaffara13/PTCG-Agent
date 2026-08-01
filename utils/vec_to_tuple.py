
def vec_to_tuple(builder: LowLevelIRBuilder, vec: Value, line: int) -> Value | None:
    return _vec_to_sequence(builder, vec, line, "to_tuple", tuple_rprimitive)

