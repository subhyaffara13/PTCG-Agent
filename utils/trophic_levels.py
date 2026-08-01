
def trophic_levels(G, weight="weight"):
    r"""Compute the trophic levels of nodes.

    The trophic level of a node $i$ is

    .. math::

        s_i = 1 + \frac{1}{k^{in}_i} \sum_{j} a_{ij} s_j

    where $k^{in}_i$ is the in-degree of i

    .. math::

        k^{in}_i = \sum_{j} a_{ij}

    and nodes with $k^{in}_i = 0$ have $s_i = 1$ by convention.

    These are calculated using the method outlined in Levine [1]_.

    Parameters
    ----------
    G : DiGraph
        A directed networkx graph

    Returns
    -------
    nodes : dict
        Dictionary of nodes with trophic level as the value.

    References
    ----------
    .. [1] Stephen Levine (1980) J. theor. Biol. 83, 195-207
    """

    basal_nodes = [n for n, deg in G.in_degree if deg == 0]
    if not basal_nodes:
        raise nx.NetworkXError(
            "This graph has no basal nodes (nodes with no incoming edges)."
            "Trophic levels are not defined without at least one basal node."
        )

    reachable_nodes = {
        node for layer in nx.bfs_layers(G, sources=basal_nodes) for node in layer
    }

    if len(reachable_nodes) != len(G.nodes):
        raise nx.NetworkXError(
            "Trophic levels are only defined for graphs where every node has a path "
            "from a basal node (basal nodes are nodes with no incoming edges)."
        )

    import numpy as np

    # find adjacency matrix
    a = nx.adjacency_matrix(G, weight=weight).T.toarray()

    # drop rows/columns where in-degree is zero
    rowsum = np.sum(a, axis=1)
    p = a[rowsum != 0][:, rowsum != 0]
    # normalise so sum of in-degree weights is 1 along each row
    p = p / rowsum[rowsum != 0][:, np.newaxis]

    # calculate trophic levels
    nn = p.shape[0]
    i = np.eye(nn)
    try:
        n = np.linalg.inv(i - p)
    except np.linalg.LinAlgError as err:
        # LinAlgError is raised when there is a non-basal node
        msg = (
            "Trophic levels are only defined for graphs where every "
            + "node has a path from a basal node (basal nodes are nodes "
            + "with no incoming edges)."
        )
        raise nx.NetworkXError(msg) from err
    y = n.sum(axis=1) + 1

    levels = {}

    # all nodes with in-degree zero have trophic level == 1
    zero_node_ids = (node_id for node_id, degree in G.in_degree if degree == 0)
    for node_id in zero_node_ids:
        levels[node_id] = 1

    # all other nodes have levels as calculated
    nonzero_node_ids = (node_id for node_id, degree in G.in_degree if degree != 0)
    for i, node_id in enumerate(nonzero_node_ids):
        levels[node_id] = y.item(i)

    return levels

