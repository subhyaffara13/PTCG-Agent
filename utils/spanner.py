
def spanner(G, stretch, weight=None, seed=None):
    """Returns a spanner of the given graph with the given stretch.

    A spanner of a graph G = (V, E) with stretch t is a subgraph
    H = (V, E_S) such that E_S is a subset of E and the distance between
    any pair of nodes in H is at most t times the distance between the
    nodes in G.

    Parameters
    ----------
    G : NetworkX graph
        An undirected simple graph.

    stretch : float
        The stretch of the spanner.

    weight : object
        The edge attribute to use as distance.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    NetworkX graph
        A spanner of the given graph with the given stretch.

    Raises
    ------
    ValueError
        If a stretch less than 1 is given.

    Notes
    -----
    This function implements the spanner algorithm by Baswana and Sen,
    see [1].

    This algorithm is a randomized las vegas algorithm: The expected
    running time is O(km) where k = (stretch + 1) // 2 and m is the
    number of edges in G. The returned graph is always a spanner of the
    given graph with the specified stretch. For weighted graphs the
    number of edges in the spanner is O(k * n^(1 + 1 / k)) where k is
    defined as above and n is the number of nodes in G. For unweighted
    graphs the number of edges is O(n^(1 + 1 / k) + kn).

    References
    ----------
    [1] S. Baswana, S. Sen. A Simple and Linear Time Randomized
    Algorithm for Computing Sparse Spanners in Weighted Graphs.
    Random Struct. Algorithms 30(4): 532-563 (2007).
    """
    if stretch < 1:
        raise ValueError("stretch must be at least 1")

    k = (stretch + 1) // 2

    # initialize spanner H with empty edge set
    H = nx.empty_graph()
    H.add_nodes_from(G.nodes)

    # phase 1: forming the clusters
    # the residual graph has V' from the paper as its node set
    # and E' from the paper as its edge set
    residual_graph = _setup_residual_graph(G, weight)
    # clustering is a dictionary that maps nodes in a cluster to the
    # cluster center
    clustering = {v: v for v in G.nodes}
    sample_prob = math.pow(G.number_of_nodes(), -1 / k)
    size_limit = 2 * math.pow(G.number_of_nodes(), 1 + 1 / k)

    i = 0
    while i < k - 1:
        # step 1: sample centers
        sampled_centers = set()
        for center in set(clustering.values()):
            if seed.random() < sample_prob:
                sampled_centers.add(center)

        # combined loop for steps 2 and 3
        edges_to_add = set()
        edges_to_remove = set()
        new_clustering = {}
        for v in residual_graph.nodes:
            if clustering[v] in sampled_centers:
                continue

            # step 2: find neighboring (sampled) clusters and
            # lightest edges to them
            lightest_edge_neighbor, lightest_edge_weight = _lightest_edge_dicts(
                residual_graph, clustering, v
            )
            neighboring_sampled_centers = (
                set(lightest_edge_weight.keys()) & sampled_centers
            )

            # step 3: add edges to spanner
            if not neighboring_sampled_centers:
                # connect to each neighboring center via lightest edge
                for neighbor in lightest_edge_neighbor.values():
                    edges_to_add.add((v, neighbor))
                # remove all incident edges
                for neighbor in residual_graph.adj[v]:
                    edges_to_remove.add((v, neighbor))

            else:  # there is a neighboring sampled center
                closest_center = min(
                    neighboring_sampled_centers, key=lightest_edge_weight.get
                )
                closest_center_weight = lightest_edge_weight[closest_center]
                closest_center_neighbor = lightest_edge_neighbor[closest_center]

                edges_to_add.add((v, closest_center_neighbor))
                new_clustering[v] = closest_center

                # connect to centers with edge weight less than
                # closest_center_weight
                for center, edge_weight in lightest_edge_weight.items():
                    if edge_weight < closest_center_weight:
                        neighbor = lightest_edge_neighbor[center]
                        edges_to_add.add((v, neighbor))

                # remove edges to centers with edge weight less than
                # closest_center_weight
                for neighbor in residual_graph.adj[v]:
                    nbr_cluster = clustering[neighbor]
                    nbr_weight = lightest_edge_weight[nbr_cluster]
                    if (
                        nbr_cluster == closest_center
                        or nbr_weight < closest_center_weight
                    ):
                        edges_to_remove.add((v, neighbor))

        # check whether iteration added too many edges to spanner,
        # if so repeat
        if len(edges_to_add) > size_limit:
            # an iteration is repeated O(1) times on expectation
            continue

        # iteration succeeded
        i = i + 1

        # actually add edges to spanner
        for u, v in edges_to_add:
            _add_edge_to_spanner(H, residual_graph, u, v, weight)

        # actually delete edges from residual graph
        residual_graph.remove_edges_from(edges_to_remove)

        # copy old clustering data to new_clustering
        for node, center in clustering.items():
            if center in sampled_centers:
                new_clustering[node] = center
        clustering = new_clustering

        # step 4: remove intra-cluster edges
        for u in residual_graph.nodes:
            for v in list(residual_graph.adj[u]):
                if clustering[u] == clustering[v]:
                    residual_graph.remove_edge(u, v)

        # update residual graph node set
        for v in list(residual_graph.nodes):
            if v not in clustering:
                residual_graph.remove_node(v)

    # phase 2: vertex-cluster joining
    for v in residual_graph.nodes:
        lightest_edge_neighbor, _ = _lightest_edge_dicts(residual_graph, clustering, v)
        for neighbor in lightest_edge_neighbor.values():
            _add_edge_to_spanner(H, residual_graph, v, neighbor, weight)

    return H

