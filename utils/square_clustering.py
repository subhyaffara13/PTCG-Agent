
def square_clustering(G, nodes=None):
    r"""Compute the squares clustering coefficient for nodes.

    For each node return the fraction of possible squares that exist at
    the node [1]_

    .. math::
       C_4(v) = \frac{ \sum_{u=1}^{k_v}
       \sum_{w=u+1}^{k_v} q_v(u,w) }{ \sum_{u=1}^{k_v}
       \sum_{w=u+1}^{k_v} [a_v(u,w) + q_v(u,w)]},

    where :math:`q_v(u,w)` are the number of common neighbors of :math:`u` and
    :math:`w` other than :math:`v` (ie squares), and :math:`a_v(u,w) = (k_u -
    (1+q_v(u,w)+\theta_{uv})) + (k_w - (1+q_v(u,w)+\theta_{uw}))`, where
    :math:`\theta_{uw} = 1` if :math:`u` and :math:`w` are connected and 0
    otherwise. [2]_

    Parameters
    ----------
    G : graph

    nodes : container of nodes, optional (default=all nodes in G)
       Compute clustering for nodes in this container.

    Returns
    -------
    c4 : dictionary
       A dictionary keyed by node with the square clustering coefficient value.

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> print(nx.square_clustering(G, 0))
    1.0
    >>> print(nx.square_clustering(G))
    {0: 1.0, 1: 1.0, 2: 1.0, 3: 1.0, 4: 1.0}

    Notes
    -----
    Self loops are ignored.

    While :math:`C_3(v)` (triangle clustering) gives the probability that
    two neighbors of node v are connected with each other, :math:`C_4(v)` is
    the probability that two neighbors of node v share a common
    neighbor different from v. This algorithm can be applied to both
    bipartite and unipartite networks.

    References
    ----------
    .. [1] Pedro G. Lind, Marta C. González, and Hans J. Herrmann. 2005
        Cycles and clustering in bipartite networks.
        Physical Review E (72) 056127.
    .. [2] Zhang, Peng et al. Clustering Coefficient and Community Structure of
        Bipartite Networks. Physica A: Statistical Mechanics and its Applications 387.27 (2008): 6869–6875.
        https://arxiv.org/abs/0710.0117v1
    """
    if nodes is None:
        node_iter = G
    else:
        node_iter = G.nbunch_iter(nodes)
    clustering = {}
    _G_adj = G._adj

    class GAdj(dict):
        """Calculate (and cache) node neighbor sets excluding self-loops."""

        def __missing__(self, v):
            v_neighbors = self[v] = set(_G_adj[v])
            v_neighbors.discard(v)  # Ignore self-loops
            return v_neighbors

    G_adj = GAdj()  # Values are sets of neighbors (no self-loops)

    for v in node_iter:
        v_neighbors = G_adj[v]
        v_degrees_m1 = len(v_neighbors) - 1  # degrees[v] - 1 (used below)
        if v_degrees_m1 <= 0:
            # Can't form a square without at least two neighbors
            clustering[v] = 0
            continue

        # Count squares with nodes u-v-w-x from the current node v.
        # Terms of the denominator: potential = uw_degrees - uw_count - triangles - squares
        # uw_degrees: degrees[u] + degrees[w] for each u-w combo
        uw_degrees = 0
        # uw_count: 1 for each u and 1 for each w for all combos (degrees * (degrees - 1))
        uw_count = len(v_neighbors) * v_degrees_m1
        # triangles: 1 for each edge where u-w or w-u are connected (i.e. triangles)
        triangles = 0
        # squares: the number of squares (also the numerator)
        squares = 0

        # Iterate over all neighbors
        for u in v_neighbors:
            u_neighbors = G_adj[u]
            uw_degrees += len(u_neighbors) * v_degrees_m1
            # P2 from https://arxiv.org/abs/2007.11111
            p2 = len(u_neighbors & v_neighbors)
            # triangles is C_3, sigma_4 from https://arxiv.org/abs/2007.11111
            # This double-counts triangles compared to `triangles` function
            triangles += p2
            # squares is C_4, sigma_12 from https://arxiv.org/abs/2007.11111
            # Include this term, b/c a neighbor u can also be a neighbor of neighbor x
            squares += p2 * (p2 - 1)  # Will divide by 2 later

        # And iterate over all neighbors of neighbors.
        # These nodes x may be the corners opposite v in squares u-v-w-x.
        two_hop_neighbors = set.union(*(G_adj[u] for u in v_neighbors))
        two_hop_neighbors -= v_neighbors  # Neighbors already counted above
        two_hop_neighbors.discard(v)
        for x in two_hop_neighbors:
            p2 = len(v_neighbors & G_adj[x])
            squares += p2 * (p2 - 1)  # Will divide by 2 later

        squares //= 2
        potential = uw_degrees - uw_count - triangles - squares
        if potential > 0:
            clustering[v] = squares / potential
        else:
            clustering[v] = 0
    if nodes in G:
        # Return the value of the sole entry in the dictionary.
        return clustering[nodes]
    return clustering

