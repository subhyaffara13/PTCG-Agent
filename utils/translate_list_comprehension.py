
def translate_list_comprehension(builder: IRBuilder, gen: GeneratorExpr) -> Value:
    if raise_error_if_contains_unreachable_names(builder, gen):
        return builder.none()

    def set_item(x: Value, y: Value, z: Value, line: int) -> None:
        builder.call_c(new_list_set_item_op, [x, y, z], line)

    # Try simplest list comprehension, otherwise fall back to general one
    val = sequence_from_generator_preallocate_helper(
        builder,
        gen,
        empty_op_llbuilder=builder.builder.new_list_op_with_length,
        set_item_op=set_item,
    )
    if val is not None:
        return val

    list_ops = builder.maybe_spill(builder.new_list_op([], gen.line))

    loop_params = list(zip(gen.indices, gen.sequences, gen.condlists, gen.is_async))

    def gen_inner_stmts() -> None:
        e = builder.accept(gen.left_expr)
        builder.primitive_op(list_append_op, [builder.read(list_ops, gen.line), e], gen.line)

    comprehension_helper(builder, loop_params, gen_inner_stmts, gen.line)
    return builder.read(list_ops, gen.line)

