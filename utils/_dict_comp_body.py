
def _dict_comp_body(builder: IRBuilder, o: DictionaryComprehension) -> Value:
    d = builder.maybe_spill(builder.call_c(dict_new_op, [], o.line))
    loop_params = list(zip(o.indices, o.sequences, o.condlists, o.is_async))

    def gen_inner_stmts() -> None:
        k = builder.accept(o.key)
        v = builder.accept(o.value)
        builder.call_c(exact_dict_set_item_op, [builder.read(d, o.line), k, v], o.line)

    comprehension_helper(builder, loop_params, gen_inner_stmts, o.line)
    return builder.read(d, o.line)

