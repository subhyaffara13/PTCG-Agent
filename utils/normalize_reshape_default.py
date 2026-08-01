
def normalize_reshape_default(match: Match, *args, **kwargs):
    reshape_node = match.nodes[0]
    if not is_node_meta_valid(reshape_node):
        log.debug("example value absent for node: %s", reshape_node)
        return
    reshape_input = get_arg_value(reshape_node, 0)

    if free_symbols(reshape_node.meta["example_value"].shape):
        log.debug("dynamic shape not supported: %s", reshape_node)
        return

    with match.graph.inserting_after(reshape_node):
        new_reshape_node = match.graph.call_function(
            torch.reshape,
            args=(reshape_input, tuple(reshape_node.meta["example_value"].shape)),
        )
    reshape_node.replace_all_uses_with(new_reshape_node)
    new_reshape_node.meta.update(reshape_node.meta)
    match.graph.erase_node(reshape_node)

