import itertools

def remove_pointless_jumps(instructions: list["Instruction"]) -> list["Instruction"]:
    """Eliminate jumps to the next instruction"""
    pointless_jumps = {
        id(a)
        for a, b in itertools.pairwise(instructions)
        if a.opname == "JUMP_ABSOLUTE" and a.target is b
    }
    return [inst for inst in instructions if id(inst) not in pointless_jumps]

