
def transform_raise_stmt(builder: IRBuilder, s: RaiseStmt) -> None:
    if s.expr is None:
        builder.call_c(reraise_exception_op, [], NO_TRACEBACK_LINE_NO)
        builder.add(Unreachable())
        return

    exc = builder.accept(s.expr)
    builder.call_c(raise_exception_op, [exc], s.line)
    builder.add(Unreachable())

