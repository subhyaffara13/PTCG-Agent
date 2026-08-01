
def transform_del_stmt(builder: IRBuilder, o: DelStmt) -> None:
    transform_del_item(builder, builder.get_assignment_target(o.expr), o.line)

