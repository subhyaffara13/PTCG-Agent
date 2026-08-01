
def transform_while_stmt(builder: IRBuilder, s: WhileStmt) -> None:
    body, next, top, else_block = BasicBlock(), BasicBlock(), BasicBlock(), BasicBlock()
    normal_loop_exit = else_block if s.else_body is not None else next

    builder.push_loop_stack(top, next)

    # Split block so that we get a handle to the top of the loop.
    builder.goto_and_activate(top)
    process_conditional(builder, s.expr, body, normal_loop_exit)

    builder.activate_block(body)
    builder.accept(s.body)
    # Add branch to the top at the end of the body.
    builder.goto(top)

    builder.pop_loop_stack()

    if s.else_body is not None:
        builder.activate_block(else_block)
        builder.accept(s.else_body)
        builder.goto(next)

    builder.activate_block(next)

