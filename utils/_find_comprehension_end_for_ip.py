
def _find_comprehension_end_for_ip(tx: InstructionTranslatorBase) -> int:
    """Find the instruction pointer of the outermost END_FOR for current comprehension."""
    assert sys.version_info >= (3, 12)
    assert tx.instruction_pointer is not None

    nesting_depth = 0
    for search_ip in range(tx.instruction_pointer, len(tx.instructions)):
        inst = tx.instructions[search_ip]
        if inst.opname == "FOR_ITER":
            nesting_depth += 1
        elif inst.opname == "END_FOR":
            nesting_depth -= 1
            if nesting_depth == 0:
                return search_ip
    return -1

