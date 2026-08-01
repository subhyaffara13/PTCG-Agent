
def get_plain_input_and_grad_nodes(
    graph: fx.Graph,
) -> dict[PlainAOTInput, tuple[fx.Node, fx.Node | None]]:
    """Get plain input nodes and their corresponding gradient nodes from a joint graph.

    Args:
        graph: The FX joint graph with descriptors

    Returns:
        A dictionary mapping each PlainAOTInput descriptor to a tuple containing:
        - The plain input node
        - The gradient (output) node if it exists, None otherwise
    """
    return {
        desc: (n, g)
        for desc, (n, g) in get_all_input_and_grad_nodes(graph).items()
        if isinstance(desc, PlainAOTInput)
    }

