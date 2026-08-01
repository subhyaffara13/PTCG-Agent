
def overwrite_instruction(
    old_inst: Instruction, new_insts: list[Instruction]
) -> list[Instruction]:
    # update old_inst.exnt_tab_entry.end if necessary
    if (
        old_inst.exn_tab_entry
        and old_inst.exn_tab_entry.end is old_inst
        and len(new_insts) > 1
    ):
        old_inst.exn_tab_entry.end = new_insts[-1]
    # preserve exception table entries and positions
    for inst in new_insts[1:]:
        inst.exn_tab_entry = copy.copy(old_inst.exn_tab_entry)
        inst.positions = old_inst.positions
    # modify old_inst in-place to preserve jump target
    old_inst.opcode = new_insts[0].opcode
    old_inst.opname = new_insts[0].opname
    old_inst.arg = new_insts[0].arg
    old_inst.argval = new_insts[0].argval
    old_inst.target = new_insts[0].target
    return [old_inst] + new_insts[1:]

