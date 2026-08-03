import sys

def create_jump_absolute(target: Instruction) -> Instruction:
    inst = "JUMP_FORWARD" if sys.version_info >= (3, 11) else "JUMP_ABSOLUTE"
    return create_instruction(inst, target=target)

