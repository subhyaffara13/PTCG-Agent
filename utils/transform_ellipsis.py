
def transform_ellipsis(builder: IRBuilder, o: EllipsisExpr) -> Value:
    return builder.add(LoadAddress(ellipsis_op.type, ellipsis_op.src, o.line))

