import copy

def virtualize_exception_table(
    exn_tab_bytes: bytes, instructions: list[Instruction]
) -> None:
    """Replace exception table entries with pointers to make editing easier"""
    exn_tab = parse_exception_table(exn_tab_bytes)
    offset_to_inst = {cast(int, inst.offset): inst for inst in instructions}
    offsets = sorted(offset_to_inst.keys())
    end_offset_idx = 0
    exn_tab_iter = iter(exn_tab)
    try:

        def step() -> tuple[ExceptionTableEntry, InstructionExnTabEntry]:
            nonlocal end_offset_idx
            entry = next(exn_tab_iter)
            # find rightmost offset <= entry.end, since entry.end may not be
            # an actual instruction, e.g. if the end instruction is LOAD_GLOBAL,
            # which takes more than 2 bytes, then entry.end points to the end
            # of the LOAD_GLOBAL instruction, not the beginning.
            while (
                end_offset_idx < len(offsets) and offsets[end_offset_idx] <= entry.end
            ):
                end_offset_idx += 1
            assert end_offset_idx > 0
            end_offset = offsets[end_offset_idx - 1]
            inst_entry = InstructionExnTabEntry(
                _get_instruction_by_offset(offset_to_inst, entry.start),  # type: ignore[arg-type]
                _get_instruction_by_offset(offset_to_inst, end_offset),  # type: ignore[arg-type]
                _get_instruction_by_offset(offset_to_inst, entry.target),  # type: ignore[arg-type]
                entry.depth,
                entry.lasti,
            )
            return entry, inst_entry

        entry, inst_entry = step()
        for inst in instructions:
            assert inst.offset is not None
            while inst.offset > entry.end:
                entry, inst_entry = step()
            if inst.offset >= entry.start:
                inst.exn_tab_entry = copy.copy(inst_entry)
    except StopIteration:
        pass

