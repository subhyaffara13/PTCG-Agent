
def transform_set_comprehension(builder: IRBuilder, o: SetComprehension) -> Value:
    gen = o.generator
    if gen in builder.comprehension_to_fitem:
        return _translate_comprehension_with_scope(
            builder, gen, lambda: translate_set_comprehension(builder, gen)
        )
    return translate_set_comprehension(builder, gen)

