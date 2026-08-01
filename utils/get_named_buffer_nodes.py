
def get_named_buffer_nodes(graph: fx.Graph) -> dict[str, fx.Node]:
    """Get buffer nodes mapped by their fully qualified names.

    This function traverses the graph to find all buffer input nodes and
    returns them in a dictionary where keys are the buffer names (FQNs)
    and values are the corresponding FX nodes.

    Args:
        graph: The FX joint graph with descriptors

    Returns:
        A dictionary mapping buffer names (str) to their corresponding FX nodes.

    Raises:
        RuntimeError: If subclass tensors are encountered (not yet supported), as
        with subclasses a FQN does not necessarily map to a single plain tensor.
    """
    r = {}
    for n in graph.nodes:
        if n.op == "placeholder":
            desc = n.meta["desc"]
            if isinstance(desc, SubclassGetAttrAOTInput):
                _raise_fqn_subclass_not_implemented(n, desc)
            elif isinstance(desc, BufferAOTInput):
                r[desc.target] = n
    return r

