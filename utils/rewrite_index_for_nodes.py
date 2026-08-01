
def rewrite_index_for_nodes(
    localize_buffer_handler: "LocalizeBufferHandler",
    index: sympy.Expr,
    global_buf_name: str,
):
    used_vars = OrderedSet(
        s for s in index.free_symbols if symbol_is_type(s, SymT.INDEX)
    )
    index_vars = []
    local_buf = localize_buffer_handler.global_to_local[global_buf_name]
    for i in range(len(local_buf.get_size())):
        var = sympy_index_symbol_with_prefix(SymT.INDEX, i)
        index_vars.append(var if var in used_vars else 0)
    index = local_buf.get_layout().make_indexer()(index_vars)
    return index

