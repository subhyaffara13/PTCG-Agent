
def remove_jump_if_none(instructions: list[Instruction]) -> None:
    new_insts = []
    for inst in instructions:
        if "_NONE" in inst.opname:
            is_op = create_instruction("IS_OP", arg=int("NOT" in inst.opname))
            # need both argval and arg set correctly now (not later)
            is_op.argval = is_op.arg

            if sys.version_info < (3, 12):
                jump_op = create_instruction(
                    (
                        "POP_JUMP_FORWARD_IF_TRUE"
                        if "FORWARD" in inst.opname
                        else "POP_JUMP_BACKWARD_IF_TRUE"
                    ),
                    target=inst.target,
                )
            else:
                jump_op = create_instruction("POP_JUMP_IF_TRUE", target=inst.target)

            replace_insts = [
                create_instruction("LOAD_CONST", argval=None),
                is_op,
                jump_op,
            ]
            new_insts.extend(overwrite_instruction(inst, replace_insts))
        else:
            new_insts.append(inst)
    instructions[:] = new_insts

