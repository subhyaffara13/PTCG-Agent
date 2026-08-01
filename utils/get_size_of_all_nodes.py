
def get_size_of_all_nodes(
    fx_module: GraphModule, args: list[torch.Tensor] | None = None
) -> None:
    """Given a fx graph module, update each node with its total size (weights + bias + output)
    and its output_size(output). For a non-module node, the total size is the output size.
    return total size"""
    if args is not None:
        # Mark shape and dtype for each node (node.shape and node.dtype)
        ShapeProp(fx_module).propagate(*args)
    # Calculate the total size of the whole fx graph
    for node in fx_module.graph.nodes:
        if node.op == "output":
            break
        node.size_bytes = get_size_of_node(fx_module, node)
    return

