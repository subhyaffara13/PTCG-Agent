
def is_jump_absolute(target: Instruction) -> bool:
    return target.opname in ("JUMP_FORWARD", "JUMP_ABSOLUTE")

