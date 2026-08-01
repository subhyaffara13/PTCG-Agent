
def _copy_comprehension_bytecode(
    tx: InstructionTranslatorBase, start_ip: int, end_ip: int
) -> list[Instruction]:
    """Copy comprehension bytecode instructions, updating jump targets."""
    inst_map: dict[Instruction, Instruction] = {}
    copied_insts: list[Instruction] = []

    for ip in range(start_ip, end_ip):
        original_inst = tx.instructions[ip]
        copied_inst = copy.copy(original_inst)
        copied_inst.exn_tab_entry = None
        inst_map[original_inst] = copied_inst
        copied_insts.append(copied_inst)

    for copied_inst in copied_insts:
        if copied_inst.target is not None and copied_inst.target in inst_map:
            copied_inst.target = inst_map[copied_inst.target]

    return copied_insts

