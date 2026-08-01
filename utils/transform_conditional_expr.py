
def transform_conditional_expr(builder: IRBuilder, expr: ConditionalExpr) -> Value:
    if_body, else_body, next_block = BasicBlock(), BasicBlock(), BasicBlock()

    process_conditional(builder, expr.cond, if_body, else_body)
    expr_type = builder.node_type(expr)
    # Having actual Phi nodes would be really nice here!
    target = Register(expr_type)

    builder.activate_block(if_body)
    with builder.builder.borrow_region(expr.line):
        true_value = builder.accept(expr.if_expr)
        true_value = builder.coerce(true_value, expr_type, expr.line)
        builder.add(Assign(target, true_value, expr.line))
    builder.goto(next_block)

    builder.activate_block(else_body)
    with builder.builder.borrow_region(expr.line):
        false_value = builder.accept(expr.else_expr)
        false_value = builder.coerce(false_value, expr_type, expr.line)
        builder.add(Assign(target, false_value, expr.line))
    builder.goto(next_block)

    builder.activate_block(next_block)

    return target

