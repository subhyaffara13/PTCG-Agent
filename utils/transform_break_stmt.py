
def transform_break_stmt(builder: IRBuilder, node: BreakStmt) -> None:
    builder.nonlocal_control[-1].gen_break(builder, node.line)

