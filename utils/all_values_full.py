
def all_values_full(args: list[Register], blocks: list[BasicBlock]) -> list[Value]:
    """Return set of all values that are initialized or accessed."""
    values: list[Value] = list(args)
    seen_registers = set(args)

    for block in blocks:
        for op in block.ops:
            for source in op.sources():
                # Look for uninitialized registers that are accessed. Ignore
                # non-registers since we don't allow ops outside basic blocks.
                if isinstance(source, Register) and source not in seen_registers:
                    values.append(source)
                    seen_registers.add(source)
            if not isinstance(op, ControlOp):
                if isinstance(op, (Assign, AssignMulti)):
                    if op.dest not in seen_registers:
                        values.append(op.dest)
                        seen_registers.add(op.dest)
                elif op.is_void:
                    continue
                else:
                    values.append(op)

    return values

