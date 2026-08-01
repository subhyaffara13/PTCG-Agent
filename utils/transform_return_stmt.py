
def transform_return_stmt(builder: IRBuilder, stmt: ReturnStmt) -> None:
    if stmt.expr:
        retval = builder.accept(stmt.expr)
    else:
        retval = builder.builder.none()
    retval = builder.coerce(retval, builder.ret_types[-1], stmt.line)
    builder.nonlocal_control[-1].gen_return(builder, retval, stmt.line)

