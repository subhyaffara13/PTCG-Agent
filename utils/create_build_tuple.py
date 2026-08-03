import sys

def create_build_tuple(n: int) -> Instruction:
    if sys.version_info >= (3, 14) and n == 0:
        return create_load_const(())
    return create_instruction("BUILD_TUPLE", arg=n)

