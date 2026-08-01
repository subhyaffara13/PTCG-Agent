
def faster_min_max(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    if expr.arg_kinds == [ARG_POS, ARG_POS]:
        x, y = builder.accept(expr.args[0]), builder.accept(expr.args[1])
        result = Register(builder.node_type(expr))
        # CPython evaluates arguments reversely when calling min(...) or max(...)
        if callee.fullname == "builtins.min":
            comparison = builder.binary_op(y, x, "<", expr.line)
        else:
            comparison = builder.binary_op(y, x, ">", expr.line)

        true_block, false_block, next_block = BasicBlock(), BasicBlock(), BasicBlock()
        builder.add_bool_branch(comparison, true_block, false_block)

        builder.activate_block(true_block)
        builder.assign(result, builder.coerce(y, result.type, expr.line), expr.line)
        builder.goto(next_block)

        builder.activate_block(false_block)
        builder.assign(result, builder.coerce(x, result.type, expr.line), expr.line)
        builder.goto(next_block)

        builder.activate_block(next_block)
        return result
    return None

