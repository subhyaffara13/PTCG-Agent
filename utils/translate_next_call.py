
def translate_next_call(builder: IRBuilder, expr: CallExpr, callee: RefExpr) -> Value | None:
    """Special case for calling next() on a generator expression, an
    idiom that shows up some in mypy.

    For example, next(x for x in l if x.id == 12, None) will
    generate code that searches l for an element where x.id == 12
    and produce the first such object, or None if no such element
    exists.
    """
    if not (
        expr.arg_kinds in ([ARG_POS], [ARG_POS, ARG_POS])
        and isinstance(expr.args[0], GeneratorExpr)
    ):
        return None

    gen = expr.args[0]
    retval = Register(builder.node_type(expr))
    default_val = builder.accept(expr.args[1]) if len(expr.args) > 1 else None
    exit_block = BasicBlock()

    def gen_inner_stmts() -> None:
        # next takes the first element of the generator, so if
        # something gets produced, we are done.
        builder.assign(retval, builder.accept(gen.left_expr), gen.left_expr.line)
        builder.goto(exit_block)

    loop_params = list(zip(gen.indices, gen.sequences, gen.condlists, gen.is_async))
    comprehension_helper(builder, loop_params, gen_inner_stmts, gen.line)

    # Now we need the case for when nothing got hit. If there was
    # a default value, we produce it, and otherwise we raise
    # StopIteration.
    if default_val:
        builder.assign(retval, default_val, gen.left_expr.line)
        builder.goto(exit_block)
    else:
        builder.add(RaiseStandardError(RaiseStandardError.STOP_ITERATION, None, expr.line))
        builder.add(Unreachable())

    builder.activate_block(exit_block)
    return retval

