
def _prepare_panther_paths(
    G,
    source,
    path_length=5,
    c=0.5,
    delta=0.1,
    eps=None,
    weight="weight",
    remove_isolates=True,
    k=None,
    seed=None,
):
    """Common preparation code for Panther similarity algorithms.

    Parameters
    ----------
    G : NetworkX graph
        A NetworkX graph
    source : node
        Source node for similarity calculation
    path_length : int
        How long the randomly generated paths should be
    c : float
        A universal constant that controls the number of random paths to generate
    delta : float
        The probability parameter for similarity approximation
    eps : float or None
        The error bound for similarity approximation
    weight : string or None
        The name of an edge attribute that holds the numerical value used as a weight
    remove_isolates : bool
        Whether to remove isolated nodes from graph processing
    k : int or None
        The number of most similar nodes to return. If provided, validates that
       ``k`` is not greater than the number of nodes in the graph.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    PantherPaths
        A tuple containing the prepared data:
        - G: The graph (possibly with isolates removed)
        - inv_node_map: Dictionary mapping node names to indices
        - index_map: Populated index map of paths
        - inv_sample_size: Inverse of sample size (for fast calculation)
        - eps: Error bound for similarity approximation
    """
    import numpy as np

    if source not in G:
        raise nx.NodeNotFound(f"Source node {source} not in G")

    isolates = set(nx.isolates(G))

    if source in isolates:
        raise nx.NetworkXUnfeasible(
            f"Panther similarity is not defined for the isolated source node {source}."
        )

    if remove_isolates:
        G = G.subgraph(node for node in G if node not in isolates).copy()

    # According to [1], they empirically determined
    # a good value for ``eps`` to be sqrt( 1 / |E| )
    if eps is None:
        eps = np.sqrt(1.0 / G.number_of_edges())

    num_nodes = G.number_of_nodes()

    # Check if k is provided and validate it against the number of nodes
    if k is not None and not remove_isolates:  # For panther_vector_similarity
        if num_nodes < k:
            raise nx.NetworkXUnfeasible(
                f"The number of requested nodes {k} is greater than the number of nodes {num_nodes}."
            )

    inv_node_map = {name: index for index, name in enumerate(G)}

    # Calculate the sample size ``R`` for how many paths
    # to randomly generate
    t_choose_2 = math.comb(path_length, 2)
    sample_size = int((c / eps**2) * (np.log2(t_choose_2) + 1 + np.log(1 / delta)))
    index_map = {}

    # Check for isolated nodes before generating random paths
    # If there are still isolated nodes in the graph after filtering,
    # they will cause issues with path generation
    remaining_isolates = set(nx.isolates(G))
    if remaining_isolates:
        raise nx.NetworkXUnfeasible(
            f"Cannot generate random paths with isolated nodes present: {remaining_isolates}"
        )

    # Generate the random paths and populate the index_map
    for _ in generate_random_paths(
        G,
        sample_size,
        path_length=path_length,
        index_map=index_map,
        weight=weight,
        seed=seed,
    ):
        # NOTE: index_map is modified in-place by `generate_random_paths`
        pass

    return (
        G,  # The graph with isolated nodes removed
        inv_node_map,
        index_map,
        1 / sample_size,
        eps,
    )

