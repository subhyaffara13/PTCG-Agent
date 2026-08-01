
def transform_dictionary_comprehension(builder: IRBuilder, o: DictionaryComprehension) -> Value:
    if raise_error_if_contains_unreachable_names(builder, o):
        return builder.none()

    if o in builder.comprehension_to_fitem:
        return _translate_comprehension_with_scope(builder, o, lambda: _dict_comp_body(builder, o))
    return _dict_comp_body(builder, o)

