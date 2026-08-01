
def insert_ref_count_opcodes(ir: FuncIR) -> None:
    """Insert reference count inc/dec opcodes to a function.

    This is the entry point to this module.
    """
    cfg = get_cfg(ir.blocks)
    values = all_values(ir.arg_regs, ir.blocks)

    borrowed = {value for value in values if value.is_borrowed}
    args: set[Value] = set(ir.arg_regs)
    live = analyze_live_regs(ir.blocks, cfg)
    borrow = analyze_borrowed_arguments(ir.blocks, cfg, borrowed)
    defined = analyze_must_defined_regs(ir.blocks, cfg, args, values, strict_errors=True)
    ordering = make_value_ordering(ir)
    cache: BlockCache = {}
    for block in ir.blocks.copy():
        if isinstance(block.ops[-1], (Branch, Goto)):
            insert_branch_inc_and_decrefs(
                block,
                cache,
                ir.blocks,
                live.before,
                borrow.before,
                borrow.after,
                defined.after,
                ordering,
            )
        transform_block(block, live.before, live.after, borrow.before, defined.after)

    cleanup_cfg(ir.blocks)

