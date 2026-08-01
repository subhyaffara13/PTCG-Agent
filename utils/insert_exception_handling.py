
def insert_exception_handling(ir: FuncIR, strict_traceback_checks: bool) -> None:
    # Generate error block if any ops may raise an exception. If an op
    # fails without its own error handler, we'll branch to this
    # block. The block just returns an error value.
    error_label: BasicBlock | None = None
    for block in ir.blocks:
        adjust_error_kinds(block)
        if error_label is None and any(op.can_raise() for op in block.ops):
            error_label = add_default_handler_block(ir)
    if error_label:
        ir.blocks = split_blocks_at_errors(
            ir.blocks, error_label, ir.traceback_name, strict_traceback_checks
        )

