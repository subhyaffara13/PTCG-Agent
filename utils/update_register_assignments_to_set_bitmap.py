
def update_register_assignments_to_set_bitmap(
    blocks: list[BasicBlock], bitmap_registers: list[Register], bitmap_backed: list[Register]
) -> None:
    """Update some assignments to registers to also set a bit in a bitmap.

    The bitmaps are used to track if a local variable has been assigned to.

    Modifies blocks.
    """
    for block in blocks:
        if any(isinstance(op, Assign) and op.dest in bitmap_backed for op in block.ops):
            new_ops: list[Op] = []
            for op in block.ops:
                if isinstance(op, Assign) and op.dest in bitmap_backed:
                    index = bitmap_backed.index(op.dest)
                    new_ops.append(op)
                    reg = bitmap_registers[index // BITMAP_BITS]
                    new = IntOp(
                        bitmap_rprimitive,
                        reg,
                        Integer(1 << (index & (BITMAP_BITS - 1)), bitmap_rprimitive),
                        IntOp.OR,
                        op.line,
                    )
                    new_ops.append(new)
                    new_ops.append(Assign(reg, new))
                else:
                    new_ops.append(op)
            block.ops = new_ops

