
def _reconstruct_block_stack(
    tx: InstructionTranslatorBase, cg: PyCodegen, cleanup: list[Instruction]
) -> None:
    """Generates bytecode to restore the block stack for running the unsupported instruction
    in the compiled bytecode."""
    # Reconstruct the context variable CLASS in the block stack
    all_txes: list[InstructionTranslatorBase] = []
    cur_tx: InstructionTranslatorBase | None = tx
    while cur_tx is not None:
        all_txes.append(cur_tx)
        cur_tx = cur_tx.parent
    for tx in reversed(all_txes):
        for b in tx.block_stack:
            # Don't exit any modes we have entered,
            # output bytecode will mutate the tf mode stack accordingly
            if isinstance(b.with_context, TorchFunctionModeVariable):
                cg.extend_output(
                    b.resume_fn().try_except_torch_function_mode(
                        cg.code_options, cleanup
                    )
                )
                continue
            assert b.with_context is not None
            assert isinstance(b.with_context, (ContextWrappingVariable))
            b.with_context.reconstruct_type(cg)
            cg.extend_output(b.resume_fn().try_finally(cg.code_options, cleanup))

