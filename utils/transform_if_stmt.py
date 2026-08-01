
def transform_if_stmt(builder: IRBuilder, stmt: IfStmt) -> None:
    if_body, next = BasicBlock(), BasicBlock()
    else_body = BasicBlock() if stmt.else_body else next

    # If statements are normalized
    assert len(stmt.expr) == 1

    process_conditional(builder, stmt.expr[0], if_body, else_body)
    builder.activate_block(if_body)
    builder.accept(stmt.body[0])
    builder.goto(next)
    if stmt.else_body:
        builder.activate_block(else_body)
        builder.accept(stmt.else_body)
        builder.goto(next)
    builder.activate_block(next)

