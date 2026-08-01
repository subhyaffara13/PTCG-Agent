
def remove_fused_load_store(instructions: list[Instruction]) -> None:
    new_insts = []
    for inst in instructions:
        if inst.opname in FUSED_INSTS:
            inst0, inst1 = FUSED_INSTS[inst.opname]
            argval0, argval1 = inst.argval

            replace_insts = [
                create_instruction(inst0, argval=argval0),
                create_instruction(inst1, argval=argval1),
            ]
            new_insts.extend(overwrite_instruction(inst, replace_insts))
        else:
            new_insts.append(inst)
    instructions[:] = new_insts

