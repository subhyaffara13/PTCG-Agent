
def check_for_uninit_using_bitmap(
    ops: list[Op],
    src: Register,
    bitmap_registers: list[Register],
    bitmap_backed: list[Register],
    error_block: BasicBlock,
    ok_block: BasicBlock,
    line: int,
) -> None:
    """Check if src is defined using a bitmap.

    Modifies ops, bitmap_registers and bitmap_backed.
    """
    if src not in bitmap_backed:
        # Set up a new bitmap backed register.
        bitmap_backed.append(src)
        n = (len(bitmap_backed) - 1) // BITMAP_BITS
        if len(bitmap_registers) <= n:
            bitmap_registers.append(Register(bitmap_rprimitive, f"__locals_bitmap{n}"))

    index = bitmap_backed.index(src)
    masked = IntOp(
        bitmap_rprimitive,
        bitmap_registers[index // BITMAP_BITS],
        Integer(1 << (index & (BITMAP_BITS - 1)), bitmap_rprimitive),
        IntOp.AND,
        line,
    )
    ops.append(masked)
    chk = ComparisonOp(masked, Integer(0, bitmap_rprimitive), ComparisonOp.EQ)
    ops.append(chk)
    ops.append(Branch(chk, error_block, ok_block, Branch.BOOL))

