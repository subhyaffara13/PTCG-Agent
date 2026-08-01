
def insert_spills(ir: FuncIR, env: ClassIR) -> None:
    cfg = get_cfg(ir.blocks, use_yields=True)
    live = analyze_live_regs(ir.blocks, cfg)
    entry_live = live.before[ir.blocks[0], 0]

    entry_live = {op for op in entry_live if not (isinstance(op, Register) and op.is_arg)}
    # TODO: Actually for now, no Registers at all -- we keep the manual spills
    entry_live = {op for op in entry_live if not isinstance(op, Register)}

    ir.blocks = spill_regs(ir.blocks, env, entry_live, live, ir.arg_regs[0])

