
def _two_sweep_undirected(G, seed):
    """Helper function for finding a lower bound on the diameter
        for undirected Graphs.

        The idea is to pick the farthest node from a random node
        and return its eccentricity.

        ``G`` is a NetworkX undirected graph.

    .. note::

        ``seed`` is a random.Random or numpy.random.RandomState instance
    """
    # select a random source node
    source = seed.choice(list(G))
    # get the distances to the other nodes
    distances = nx.shortest_path_length(G, source)
    # if some nodes have not been visited, then the graph is not connected
    if len(distances) != len(G):
        raise nx.NetworkXError("Graph not connected.")
    # take a node that is (one of) the farthest nodes from the source
    *_, node = distances
    # return the eccentricity of the node
    return nx.eccentricity(G, node)

