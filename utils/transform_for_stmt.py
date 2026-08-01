
def transform_for_stmt(builder: IRBuilder, s: ForStmt) -> None:
    def body() -> None:
        builder.accept(s.body)

    def else_block() -> None:
        assert s.else_body is not None
        builder.accept(s.else_body)

    for_loop_helper(
        builder, s.index, s.expr, body, else_block if s.else_body else None, s.is_async, s.line
    )

