
def generate_random_paths(
    G,
    sample_size,
    path_length=5,
    index_map=None,
    weight="weight",
    seed=None,
    *,
    source=None,
):
    """Randomly generate `sample_size` paths of length `path_length`.

    Parameters
    ----------
    G : NetworkX graph
        A NetworkX graph
    sample_size : integer
        The number of paths to generate. This is ``R`` in [1]_.
    path_length : integer (default = 5)
        The maximum size of the path to randomly generate.
        This is ``T`` in [1]_. According to the paper, ``T >= 5`` is
        recommended.
    index_map : dictionary, optional
        If provided, this will be populated with the inverted
        index of nodes mapped to the set of generated random path
        indices within ``paths``.
    weight : string or None, optional (default="weight")
        The name of an edge attribute that holds the numerical value
        used as a weight. If None then each edge has weight 1.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
    source : node, optional
        Node to use as the starting point for all generated paths.
        If None then starting nodes are selected at random with uniform probability.

    Returns
    -------
    paths : generator of lists
        Generator of `sample_size` paths each with length `path_length`.

    Examples
    --------
    The generator yields `sample_size` number of paths of length `path_length`
    drawn from `G`:

    >>> G = nx.complete_graph(5)
    >>> next(nx.generate_random_paths(G, sample_size=1, path_length=3, seed=42))
    [3, 4, 2, 3]
    >>> list(nx.generate_random_paths(G, sample_size=3, path_length=4, seed=42))
    [[3, 4, 2, 3, 0], [2, 0, 2, 1, 0], [2, 0, 4, 3, 0]]

    By passing a dictionary into `index_map`, it will build an
    inverted index mapping of nodes to the paths in which that node is present:

    >>> G = nx.wheel_graph(10)
    >>> index_map = {}
    >>> random_paths = list(
    ...     nx.generate_random_paths(G, sample_size=3, index_map=index_map, seed=2771)
    ... )
    >>> random_paths
    [[3, 2, 1, 9, 8, 7], [4, 0, 5, 6, 7, 8], [3, 0, 5, 0, 9, 8]]
    >>> paths_containing_node_0 = [
    ...     random_paths[path_idx] for path_idx in index_map.get(0, [])
    ... ]
    >>> paths_containing_node_0
    [[4, 0, 5, 6, 7, 8], [3, 0, 5, 0, 9, 8]]

    References
    ----------
    .. [1] Zhang, J., Tang, J., Ma, C., Tong, H., Jing, Y., & Li, J.
           Panther: Fast top-k similarity search on large networks.
           In Proceedings of the ACM SIGKDD International Conference
           on Knowledge Discovery and Data Mining (Vol. 2015-August, pp. 1445–1454).
           Association for Computing Machinery. https://doi.org/10.1145/2783258.2783267.
    """
    import numpy as np

    randint_fn = (
        seed.integers if isinstance(seed, np.random.Generator) else seed.randint
    )

    # Calculate transition probabilities between
    # every pair of vertices according to Eq. (3)
    adj_mat = nx.to_numpy_array(G, weight=weight)

    # Handle isolated nodes by checking for zero row sums
    row_sums = adj_mat.sum(axis=1).reshape(-1, 1)
    inv_row_sums = np.reciprocal(row_sums)
    transition_probabilities = adj_mat * inv_row_sums

    node_map = list(G)
    num_nodes = G.number_of_nodes()

    for path_index in range(sample_size):
        if source is None:
            # Sample current vertex v = v_i uniformly at random
            node_index = randint_fn(num_nodes)
            node = node_map[node_index]
        else:
            if source not in node_map:
                raise nx.NodeNotFound(f"Initial node {source} not in G")

            node = source
            node_index = node_map.index(node)

        # Add v into p_r and add p_r into the path set
        # of v, i.e., P_v
        path = [node]

        # Build the inverted index (P_v) of vertices to paths
        if index_map is not None:
            if node in index_map:
                index_map[node].add(path_index)
            else:
                index_map[node] = {path_index}

        starting_index = node_index
        for _ in range(path_length):
            # Randomly sample a neighbor (v_j) according
            # to transition probabilities from ``node`` (v) to its neighbors
            nbr_index = seed.choice(
                num_nodes, p=transition_probabilities[starting_index]
            )

            # Set current vertex (v = v_j)
            starting_index = nbr_index

            # Add v into p_r
            nbr_node = node_map[nbr_index]
            path.append(nbr_node)

            # Add p_r into P_v
            if index_map is not None:
                if nbr_node in index_map:
                    index_map[nbr_node].add(path_index)
                else:
                    index_map[nbr_node] = {path_index}

        yield path

