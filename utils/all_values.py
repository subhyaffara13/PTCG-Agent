
def all_values(args: list[Register], blocks: list[BasicBlock]) -> list[Value]:
    """Return the set of all values that may be initialized in the blocks.

    This omits registers that are only read.
    """
    values: list[Value] = list(args)
    seen_registers = set(args)

    for block in blocks:
        for op in block.ops:
            if not isinstance(op, ControlOp):
                if isinstance(op, (Assign, AssignMulti)):
                    if op.dest not in seen_registers:
                        values.append(op.dest)
                        seen_registers.add(op.dest)
                elif op.is_void:
                    continue
                else:
                    # If we take the address of a register, it might get initialized.
                    if (
                        isinstance(op, LoadAddress)
                        and isinstance(op.src, Register)
                        and op.src not in seen_registers
                    ):
                        values.append(op.src)
                        seen_registers.add(op.src)
                    values.append(op)

    return values

