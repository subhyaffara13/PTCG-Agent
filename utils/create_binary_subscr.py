import sys

def create_binary_subscr() -> Instruction:
    if sys.version_info < (3, 14):
        return create_instruction("BINARY_SUBSCR")
    # https://github.com/python/cpython/blob/0e46c0499413bc5f9f8336fe76e2e67cf93f64d8/Include/opcode.h#L36
    return create_instruction("BINARY_OP", arg=26)

