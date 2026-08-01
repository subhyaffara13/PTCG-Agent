
def transform_operator_assignment_stmt(builder: IRBuilder, stmt: OperatorAssignmentStmt) -> None:
    """Operator assignment statement such as x += 1"""
    builder.disallow_class_assignments([stmt.lvalue], stmt.line)
    if (
        is_tagged(builder.node_type(stmt.lvalue))
        and is_tagged(builder.node_type(stmt.rvalue))
        and stmt.op in int_borrow_friendly_op
    ):
        can_borrow = is_borrow_friendly_expr(builder, stmt.rvalue) and is_borrow_friendly_expr(
            builder, stmt.lvalue
        )
    else:
        can_borrow = False
    target = builder.get_assignment_target(stmt.lvalue)
    target_value = builder.read(target, stmt.line, can_borrow=can_borrow)
    rreg = builder.accept(stmt.rvalue, can_borrow=can_borrow)
    # the Python parser strips the '=' from operator assignment statements, so re-add it
    op = stmt.op + "="
    res = builder.binary_op(target_value, rreg, op, stmt.line)
    # usually operator assignments are done in-place
    # but when target doesn't support that we need to manually assign
    builder.assign(target, res, res.line)
    builder.flush_keep_alives(res.line)

