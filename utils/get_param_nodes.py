
def get_param_nodes(graph: fx.Graph) -> list[fx.Node]:
    """Get all parameter nodes from a graph as a list.

    You can rely on this providing the correct order of parameters you need
    to feed into the joint graph (at the very beginning of the argument list,
    before buffers).

    Args:
        graph: The FX joint graph with descriptors

    Returns:
        A list of FX nodes representing all parameters in the graph.

    Raises:
        RuntimeError: If subclass tensors are encountered (not yet supported), as
        it is not clear if you wanted each individual constituent piece of the
        subclasses, or have them grouped up in some way.
    """
    return list(get_named_param_nodes(graph).values())

