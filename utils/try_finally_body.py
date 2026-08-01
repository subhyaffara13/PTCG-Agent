
def try_finally_body(
    builder: IRBuilder, finally_block: BasicBlock, finally_body: GenFunc, old_exc: Value
) -> tuple[BasicBlock, FinallyNonlocalControl]:
    cleanup_block = BasicBlock()
    # Compile the finally block with the nonlocal control flow overridden to restore exc_info
    builder.builder.push_error_handler(cleanup_block)
    finally_control = FinallyNonlocalControl(builder.nonlocal_control[-1], old_exc)
    builder.nonlocal_control.append(finally_control)
    builder.activate_block(finally_block)
    finally_body()
    builder.nonlocal_control.pop()

    return cleanup_block, finally_control

