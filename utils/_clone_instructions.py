
def _clone_instructions(instructions: Sequence[Instruction]) -> list[Instruction]:
    # This is super hot and this is the fastest way to do this (tried copy.copy
    # and dataclasses.replace).
    copied = [
        Instruction(
            i.opcode,
            i.opname,
            i.arg,
            i.argval,
            i.offset,
            i.starts_line,
            i.is_jump_target,
            i.positions,
            i.target,
            i.exn_tab_entry,
            i.argrepr,
        )
        for i in instructions
    ]

    remap = dict(zip(instructions, copied))
    # Handle `None` in the remapper so we don't need an extra `if`.
    remap[None] = None  # type: ignore[index, assignment]

    for i in copied:
        i.target = remap[i.target]  # type: ignore[index]
        if entry := i.exn_tab_entry:
            i.exn_tab_entry = InstructionExnTabEntry(
                remap[entry.start],
                remap[entry.end],
                remap[entry.target],
                entry.depth,
                entry.lasti,
            )
    return copied

