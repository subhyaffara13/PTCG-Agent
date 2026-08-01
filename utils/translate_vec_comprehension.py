
def translate_vec_comprehension(
    builder: IRBuilder, vec_type: RVec, gen: GeneratorExpr, *, capacity: Value | None = None
) -> Value:
    def set_item(x: Value, y: Value, z: Value, line: int) -> None:
        vec_init_item_unsafe(builder.builder, x, y, z, line)

    # Try simplest comprehension, otherwise fall back to general one
    val = sequence_from_generator_preallocate_helper(
        builder,
        gen,
        empty_op_llbuilder=lambda length, line: vec_create(
            builder.builder, vec_type, length, line, capacity=capacity
        ),
        set_item_op=set_item,
    )
    if val is not None:
        return val

    vec = Register(vec_type)
    builder.assign(
        vec, vec_create(builder.builder, vec_type, 0, gen.line, capacity=capacity), gen.line
    )
    loop_params = list(zip(gen.indices, gen.sequences, gen.condlists, gen.is_async))

    def gen_inner_stmts() -> None:
        e = builder.accept(gen.left_expr)
        builder.assign(vec, vec_append(builder.builder, vec, e, gen.line), gen.line)

    comprehension_helper(builder, loop_params, gen_inner_stmts, gen.line)
    return vec

