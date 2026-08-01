
def create_load_method(name: str) -> Instruction:
    if sys.version_info >= (3, 12):
        # in 3.12, create a LOAD_ATTR instruction with the low bit set
        return create_instruction("LOAD_ATTR", arg=1, argval=name)
    return create_instruction("LOAD_METHOD", argval=name)

