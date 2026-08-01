
def _unflatten_graph(space: Graph, x: GraphInstance) -> GraphInstance:
    """We're not using `.unflatten() for :class:`Box` and :class:`Discrete` because a graph is not a homogeneous space.

    The size of the outcome is actually not fixed, but determined based on the number of
    nodes and edges in the graph.
    """

    def _graph_unflatten(unflatten_space, unflatten_x):
        result = None
        if unflatten_space is not None and unflatten_x is not None:
            if isinstance(unflatten_space, Box):
                result = unflatten_x.reshape(-1, *unflatten_space.shape)
            elif isinstance(unflatten_space, Discrete):
                result = np.asarray(np.nonzero(unflatten_x))[-1, :]
        return result

    nodes = _graph_unflatten(space.node_space, x.nodes)
    edges = _graph_unflatten(space.edge_space, x.edges)

    return GraphInstance(nodes, edges, x.edge_links)


def _unflatten_graph(space: Graph, x: GraphInstance) -> GraphInstance:
    """We're not using `.unflatten() for :class:`Box` and :class:`Discrete` because a graph is not a homogeneous space.

    The size of the outcome is actually not fixed, but determined based on the number of
    nodes and edges in the graph.
    """

    def _graph_unflatten(space, x):
        ret = None
        if space is not None and x is not None:
            if isinstance(space, Box):
                ret = x.reshape(-1, *space.shape)
            elif isinstance(space, Discrete):
                ret = np.asarray(np.nonzero(x))[-1, :]
        return ret

    nodes = _graph_unflatten(space.node_space, x.nodes)
    edges = _graph_unflatten(space.edge_space, x.edges)

    return GraphInstance(nodes, edges, x.edge_links)

