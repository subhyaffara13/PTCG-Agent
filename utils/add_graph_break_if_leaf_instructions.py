
def add_graph_break_if_leaf_instructions(instructions: list[Instruction]) -> None:
    new_insts = []
    for inst in instructions:
        if "RETURN" in inst.opname:
            replace_insts = [
                create_instruction("NOP", argval="GRAPH_BREAK_IF_LEAF"),
                create_instruction(inst.opname, argval=inst.argval),
            ]
            new_insts.extend(overwrite_instruction(inst, replace_insts))
        else:
            new_insts.append(inst)
    instructions[:] = new_insts

