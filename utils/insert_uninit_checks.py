
def insert_uninit_checks(ir: FuncIR, strict_traceback_checks: bool) -> None:
    # Remove dead blocks from the CFG, which helps avoid spurious
    # checks due to unused error handling blocks.
    cleanup_cfg(ir.blocks)

    cfg = get_cfg(ir.blocks)
    must_defined = analyze_must_defined_regs(
        ir.blocks, cfg, set(ir.arg_regs), all_values(ir.arg_regs, ir.blocks)
    )

    ir.blocks = split_blocks_at_uninits(ir.blocks, must_defined.before, strict_traceback_checks)

