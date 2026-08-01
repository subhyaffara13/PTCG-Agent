
def _get_instruction_by_offset(
    offset_to_inst: dict[int, Instruction], offset: int
) -> Instruction | None:
    """
    Get the instruction located at a given offset, accounting for EXTENDED_ARGs
    """
    for n in (0, 2, 4, 6):
        if offset_to_inst[offset + n].opcode != dis.EXTENDED_ARG:
            return offset_to_inst[offset + n]
    return None

