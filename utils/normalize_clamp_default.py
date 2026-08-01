
def normalize_clamp_default(match: Match, *args, **kwargs):
    clamp_node = match.nodes[0]
    if not is_node_meta_valid(clamp_node):
        log.debug("example value absent for node: %s", clamp_node)
        return

    if free_symbols(clamp_node.meta["example_value"].shape):
        log.debug("dynamic shape not supported: %s", clamp_node)
        return
    if len(clamp_node.args) > 1:
        args = (get_arg_value(clamp_node, 0),)
        kwargs = {
            "min": get_arg_value(clamp_node, 1, kwarg_name="min"),
            "max": get_arg_value(clamp_node, 2, kwarg_name="max"),
        }
    else:
        args = clamp_node.args
        kwargs = clamp_node.kwargs
    with match.graph.inserting_after(clamp_node):
        new_clamp_node = match.graph.call_function(
            torch.clamp,
            args=args,
            kwargs=kwargs,
        )
    clamp_node.replace_all_uses_with(new_clamp_node)
    new_clamp_node.meta.update(clamp_node.meta)
    match.graph.erase_node(clamp_node)

