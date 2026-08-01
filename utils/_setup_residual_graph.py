
def _setup_residual_graph(G, weight):
    """Setup residual graph as a copy of G with unique edges weights.

    The node set of the residual graph corresponds to the set V' from
    the Baswana-Sen paper and the edge set corresponds to the set E'
    from the paper.

    This function associates distinct weights to the edges of the
    residual graph (even for unweighted input graphs), as required by
    the algorithm.

    Parameters
    ----------
    G : NetworkX graph
        An undirected simple graph.

    weight : object
        The edge attribute to use as distance.

    Returns
    -------
    NetworkX graph
        The residual graph used for the Baswana-Sen algorithm.
    """
    residual_graph = G.copy()

    # establish unique edge weights, even for unweighted graphs
    for u, v in G.edges():
        if not weight:
            residual_graph[u][v]["weight"] = (id(u), id(v))
        else:
            residual_graph[u][v]["weight"] = (G[u][v][weight], id(u), id(v))

    return residual_graph

