
def normalize_unbind_default(match: Match, *args, **kwargs):
    node = match.nodes[0]
    graph = match.graph
    input = get_arg_value(node, 0, "input")
    dim = get_arg_value(node, 1, "dim")
    if dim is None:
        axis = node.kwargs.get("axis")
        if axis is not None:
            dim = axis
        else:
            dim = 0
    if input is None:
        log.debug("couldn't find unbind args")
        return
    if not is_node_meta_valid(input):
        log.debug("example value absent for node: %s", input)
        return
    ndim = input.meta["example_value"].ndim

    if dim < 0:  # Normalize unbind dim
        dim += ndim
    with graph.inserting_after(node):
        new_node = graph.call_function(
            torch.unbind,
            args=(input,),
            kwargs={"dim": dim},
        )
    node.replace_all_uses_with(new_node)
    new_node.meta.update(node.meta)
    graph.erase_node(node)
    counters[backend]["normalization_pass"] += 1

