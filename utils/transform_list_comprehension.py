
def transform_list_comprehension(builder: IRBuilder, o: ListComprehension) -> Value:
    gen = o.generator
    if gen in builder.comprehension_to_fitem:
        return _translate_comprehension_with_scope(
            builder, gen, lambda: translate_list_comprehension(builder, gen)
        )
    return translate_list_comprehension(builder, gen)

