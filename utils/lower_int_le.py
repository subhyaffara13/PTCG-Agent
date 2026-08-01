
def lower_int_le(builder: LowLevelIRBuilder, args: list[Value], line: int) -> Value:
    return compare_tagged(builder, args[0], args[1], "<=", line)

