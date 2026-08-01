
def make_value_ordering(ir: FuncIR) -> dict[Value, int]:
    """Create a ordering of values that allows them to be sorted.

    This omits registers that are only ever read.
    """
    # TODO: Never initialized values??
    result: dict[Value, int] = {}
    n = 0

    for arg in ir.arg_regs:
        result[arg] = n
        n += 1

    for block in ir.blocks:
        for op in block.ops:
            if (
                isinstance(op, LoadAddress)
                and isinstance(op.src, Register)
                and op.src not in result
            ):
                # Taking the address of a register allows initialization.
                result[op.src] = n
                n += 1
            if isinstance(op, Assign):
                if op.dest not in result:
                    result[op.dest] = n
                    n += 1
            elif op not in result:
                result[op] = n
                n += 1

    return result

