
def check_offsets(instructions: Sequence[Instruction]) -> None:
    offset = 0
    for inst in instructions:
        assert inst.offset == offset
        offset += instruction_size(inst)

