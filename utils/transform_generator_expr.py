
def transform_generator_expr(builder: IRBuilder, o: GeneratorExpr) -> Value:
    builder.warning("Treating generator comprehension as list", o.line)
    if o in builder.comprehension_to_fitem:
        return builder.primitive_op(
            iter_op,
            [
                _translate_comprehension_with_scope(
                    builder, o, lambda: translate_list_comprehension(builder, o)
                )
            ],
            o.line,
        )
    return builder.primitive_op(iter_op, [translate_list_comprehension(builder, o)], o.line)

