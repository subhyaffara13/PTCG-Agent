
def transform_try_finally_stmt(
    builder: IRBuilder, try_body: GenFunc, finally_body: GenFunc, line: int = -1
) -> None:
    """Generalized try/finally handling that takes functions to gen the bodies.

    The point of this is to also be able to support with."""
    # Finally is a big pain, because there are so many ways that
    # exits can occur. We emit 10+ basic blocks for every finally!

    err_handler, main_entry, return_entry, finally_block = (
        BasicBlock(),
        BasicBlock(),
        BasicBlock(),
        BasicBlock(),
    )

    # Compile the body of the try
    ret_reg = try_finally_try(builder, err_handler, return_entry, main_entry, try_body)

    # Set up the entry blocks for the finally statement
    old_exc = try_finally_entry_blocks(
        builder, err_handler, return_entry, main_entry, finally_block, ret_reg
    )

    # Compile the body of the finally
    cleanup_block, finally_control = try_finally_body(
        builder, finally_block, finally_body, old_exc
    )

    # Resolve the control flow out of the finally block
    out_block = try_finally_resolve_control(
        builder, cleanup_block, finally_control, old_exc, ret_reg
    )

    builder.activate_block(out_block)

