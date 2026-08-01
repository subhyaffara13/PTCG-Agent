
def get_param_and_grad_nodes(
    graph: fx.Graph,
) -> dict[ParamAOTInput, tuple[fx.Node, fx.Node | None]]:
    """Get parameter nodes and their corresponding gradient nodes from a joint graph.

    Args:
        graph: The FX joint graph with descriptors

    Returns:
        A dictionary mapping each ParamAOTInput descriptor to a tuple containing:
        - The parameter input node
        - The gradient (output) node if it exists, None otherwise
    """
    return {
        desc: (n, g)
        for desc, (n, g) in get_all_input_and_grad_nodes(graph).items()
        if isinstance(desc, ParamAOTInput)
    }

