
def transform_continue_stmt(builder: IRBuilder, node: ContinueStmt) -> None:
    builder.nonlocal_control[-1].gen_continue(builder, node.line)

