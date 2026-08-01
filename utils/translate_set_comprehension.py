
def translate_set_comprehension(builder: IRBuilder, gen: GeneratorExpr) -> Value:
    if raise_error_if_contains_unreachable_names(builder, gen):
        return builder.none()

    set_ops = builder.maybe_spill(builder.new_set_op([], gen.line))
    loop_params = list(zip(gen.indices, gen.sequences, gen.condlists, gen.is_async))

    def gen_inner_stmts() -> None:
        e = builder.accept(gen.left_expr)
        builder.primitive_op(set_add_op, [builder.read(set_ops, gen.line), e], gen.line)

    comprehension_helper(builder, loop_params, gen_inner_stmts, gen.line)
    return builder.read(set_ops, gen.line)

