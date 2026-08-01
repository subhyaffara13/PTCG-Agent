
def virtualize_jumps(instructions: Iterable[Instruction]) -> None:
    """Replace jump targets with pointers to make editing easier"""
    jump_targets = {
        inst.offset: inst for inst in instructions if inst.offset is not None
    }

    for inst in instructions:
        if inst.opcode in dis.hasjabs or inst.opcode in dis.hasjrel:
            inst.target = _get_instruction_by_offset(jump_targets, inst.argval)

