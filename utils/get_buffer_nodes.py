
def get_buffer_nodes(graph: fx.Graph) -> list[fx.Node]:
    """Get all buffer nodes from a graph as a list.

    You can rely on this providing the correct order of buffers you need
    to feed into the joint graph (after parameters).

    Args:
        graph: The FX joint graph with descriptors

    Returns:
        A list of FX nodes representing all buffers in the graph.

    Raises:
        RuntimeError: If subclass tensors are encountered (not yet supported), as
        it is not clear if you wanted each individual constituent piece of the
        subclasses, or have them grouped up in some way.
    """
    return list(get_named_buffer_nodes(graph).values())

