
def transform_assignment_expr(builder: IRBuilder, o: AssignmentExpr) -> Value:
    value = builder.accept(o.value)
    target = builder.get_assignment_target(o.target)
    builder.assign(target, value, o.line)
    return value

