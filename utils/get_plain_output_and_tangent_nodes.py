
def get_plain_output_and_tangent_nodes(
    graph: fx.Graph,
) -> dict[PlainAOTOutput, tuple[fx.Node, fx.Node | None]]:
    """Get plain output nodes and their corresponding tangent nodes from a joint graph.

    Args:
        graph: The FX joint graph with descriptors

    Returns:
        A dictionary mapping each PlainAOTOutput descriptor to a tuple containing:
        - The plain output node
        - The tangent (input) node if it exists, None otherwise
    """
    return {
        desc: (n, g)
        for desc, (n, g) in get_all_output_and_tangent_nodes(graph).items()
        if isinstance(desc, PlainAOTOutput)
    }

