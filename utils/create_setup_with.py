import sys

def create_setup_with(target: Instruction) -> Instruction:
    opname = "BEFORE_WITH" if sys.version_info >= (3, 11) else "SETUP_WITH"
    return create_instruction(opname, target=target)

