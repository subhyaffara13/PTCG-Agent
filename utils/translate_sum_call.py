
def translate_sum_call(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    # specialized implementation is used if:
    # - only one or two arguments given (if not, sum() has been given invalid arguments)
    # - first argument is a Generator (there is no benefit to optimizing the performance of eg.
    #   sum([1, 2, 3]), so non-Generator Iterables are not handled)
    if not (
        len(expr.args) in (1, 2)
        and expr.arg_kinds[0] == ARG_POS
        and isinstance(expr.args[0], GeneratorExpr)
    ):
        return None

    # handle 'start' argument, if given
    if len(expr.args) == 2:
        # ensure call to sum() was properly constructed
        if expr.arg_kinds[1] not in (ARG_POS, ARG_NAMED):
            return None
        start_expr = expr.args[1]
    else:
        start_expr = IntExpr(0)

    gen_expr = expr.args[0]
    target_type = builder.node_type(expr)
    retval = Register(target_type, line=expr.line)
    builder.assign(
        retval, builder.coerce(builder.accept(start_expr), target_type, expr.line), expr.line
    )

    def gen_inner_stmts() -> None:
        call_expr = builder.accept(gen_expr.left_expr)
        builder.assign(
            retval, builder.binary_op(retval, call_expr, "+", call_expr.line), call_expr.line
        )

    loop_params = list(
        zip(gen_expr.indices, gen_expr.sequences, gen_expr.condlists, gen_expr.is_async)
    )
    comprehension_helper(builder, loop_params, gen_inner_stmts, gen_expr.line)

    return retval

