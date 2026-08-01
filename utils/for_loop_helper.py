
def for_loop_helper(
    builder: IRBuilder,
    index: Lvalue,
    expr: Expression,
    body_insts: GenFunc,
    else_insts: GenFunc | None,
    is_async: bool,
    line: int,
) -> None:
    """Generate IR for a loop.

    Args:
        index: the loop index Lvalue
        expr: the expression to iterate over
        body_insts: a function that generates the body of the loop
        else_insts: a function that generates the else block instructions
    """
    # Body of the loop
    body_block = BasicBlock()
    # Block that steps to the next item
    step_block = BasicBlock()
    # Block for the else clause, if we need it
    else_block = BasicBlock()
    # Block executed after the loop
    exit_block = BasicBlock()

    # Determine where we want to exit, if our condition check fails.
    normal_loop_exit = else_block if else_insts is not None else exit_block

    for_gen = make_for_loop_generator(
        builder, index, expr, body_block, normal_loop_exit, line, is_async=is_async
    )

    builder.push_loop_stack(step_block, exit_block)
    condition_block = BasicBlock()
    builder.goto_and_activate(condition_block)

    # Add loop condition check.
    for_gen.gen_condition()

    # Generate loop body.
    builder.activate_block(body_block)
    for_gen.begin_body()
    body_insts()

    # We generate a separate step block (which might be empty).
    builder.goto_and_activate(step_block)
    for_gen.gen_step()
    # Go back to loop condition.
    builder.goto(condition_block)

    for_gen.add_cleanup(normal_loop_exit)
    builder.pop_loop_stack()

    if else_insts is not None:
        builder.activate_block(else_block)
        else_insts()
        builder.goto(exit_block)

    builder.activate_block(exit_block)

