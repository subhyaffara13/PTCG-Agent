
def normalize_detach_default(match: Match, *args, **kwargs):
    detach_node = match.nodes[0]
    if not is_node_meta_valid(detach_node):
        log.debug("example value absent for node: %s", detach_node)
        return

    if free_symbols(detach_node.meta["example_value"].shape):
        log.debug("dynamic shape not supported: %s", detach_node)
        return

    with match.graph.inserting_after(detach_node):
        new_detach_node = match.graph.call_function(
            torch.detach,
            args=detach_node.args,
        )
    detach_node.replace_all_uses_with(new_detach_node)
    new_detach_node.meta.update(detach_node.meta)
    match.graph.erase_node(detach_node)

