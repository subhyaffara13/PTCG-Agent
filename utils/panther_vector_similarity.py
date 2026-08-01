
def panther_vector_similarity(
    G,
    source,
    *,
    D=10,
    k=5,
    path_length=5,
    c=0.5,
    delta=0.1,
    eps=None,
    weight="weight",
    seed=None,
):
    r"""Returns the Panther vector similarity (Panther++) of nodes in `G`.

    Computes similarity between nodes based on the "Panther++" algorithm [1]_, which extends
    the basic Panther algorithm by using feature vectors to better capture structural
    similarity.

    While basic Panther similarity measures how often two nodes appear on the same paths,
    Panther vector similarity (Panther++) creates a ``D``-dimensional feature vector for each
    node using its top similarity scores with other nodes, then computes similarity based
    on the Euclidean distance between these feature vectors. This approach better captures
    structural similarity and addresses the bias towards close neighbors present in
    the original Panther algorithm.

    This approach is preferred when:

    1. You need better structural similarity than basic path co-occurrence
    2. You want to overcome the close-neighbor bias of standard Panther
    3. You're working with large graphs where k-d tree indexing would be beneficial
    4. Graph edit distance-like similarity is more appropriate than path co-occurrence

    Parameters
    ----------
    G : NetworkX graph
        A NetworkX graph
    source : node
        Source node for which to find the top ``k`` similar other nodes
    D : int
        The number of similarity scores to use (in descending order)
        for each feature vector. Defaults to 10. Note that the original paper
        used D=50 [1]_, but KDTree is optimized for lower dimensions.
    k : int
        The number of most similar nodes to return
    path_length : int
        How long the randomly generated paths should be (``T`` in [1]_)
    c : float
        A universal constant that controls the number of random paths to generate.
        Higher values increase the number of sample paths and potentially improve
        accuracy at the cost of more computation. Defaults to 0.5 as recommended
        in [1]_.
    delta : float
        The probability that ``S`` is not an epsilon-approximation to (R, phi)
    eps : float
        The error bound for similarity approximation. This controls the accuracy
        of the sampled paths in representing the true similarity. Smaller values
        yield more accurate results but require more sample paths. If None, a
        value of ``sqrt(1/|E|)`` is used, which the authors found empirically
        effective.
    weight : string or None, optional (default="weight")
        The name of an edge attribute that holds the numerical value
        used as a weight. If `None` then each edge has weight 1.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    similarity : dict
        Dict of nodes to similarity scores (as floats).
        Note: the self-similarity (i.e., `node`) is not included in the dict.

    Examples
    --------
    >>> G = nx.star_graph(100)

    The "hub" node is distinct from the "spoke" nodes

    >>> from pprint import pprint
    >>> pprint(nx.panther_vector_similarity(G, source=0, seed=42))
    {35: 0.10402634656233918,
     61: 0.10434063328712018,
     65: 0.10401247833456054,
     85: 0.10506718868571752,
     88: 0.10402634656233918}

    But "spoke" nodes are similar to one another

    >>> result = nx.panther_vector_similarity(G, source=1, seed=42)
    >>> len(result)
    5
    >>> all(similarity == 1.0 for similarity in result.values())
    True

    Notes
    -----
    Results may be nondeterministic when feature vectors have the same distances,
    as the KDTree's internal tie-breaking behavior can vary between runs.
    Using the same ``seed`` parameter ensures reproducible results.

    References
    ----------
    .. [1] Zhang, J., Tang, J., Ma, C., Tong, H., Jing, Y., & Li, J.
           Panther: Fast top-k similarity search on large networks.
           In Proceedings of the ACM SIGKDD International Conference
           on Knowledge Discovery and Data Mining (Vol. 2015-August, pp. 1445–1454).
           Association for Computing Machinery. https://doi.org/10.1145/2783258.2783267.
    """
    import numpy as np
    import scipy as sp

    # Use helper method to prepare common data structures but keep isolates in the graph
    G, inv_node_map, index_map, inv_sample_size, eps = _prepare_panther_paths(
        G,
        source,
        path_length=path_length,
        c=c,
        delta=delta,
        eps=eps,
        weight=weight,
        remove_isolates=False,
        k=k,
        seed=seed,
    )
    num_nodes = G.number_of_nodes()
    node_list = list(G.nodes)

    # Ensure D doesn't exceed the number of nodes
    if num_nodes < D:
        raise nx.NetworkXUnfeasible(
            f"The number of requested similarity scores {D} is greater than the number of nodes {num_nodes}."
        )

    similarities = np.zeros((num_nodes, num_nodes))
    theta = np.zeros((num_nodes, D))
    index_map_sets = {node: set(paths) for node, paths in index_map.items()}

    # Calculate the path similarities for each node
    for vi_idx, vi in enumerate(G.nodes):
        vi_paths = index_map_sets[vi]

        for node, node_paths in index_map_sets.items():
            # Calculate similarity score
            common_path_count = len(vi_paths.intersection(node_paths))
            similarities[vi_idx, inv_node_map[node]] = (
                common_path_count * inv_sample_size
            )

        # Build up the feature vector using the largest D similarity scores
        theta[vi_idx] = np.sort(np.partition(similarities[vi_idx], -D)[-D:])[::-1]

    # Insert the feature vectors into a k-d tree
    # for fast retrieval
    kdtree = sp.spatial.KDTree(theta)

    # Retrieve top ``k+1`` similar vertices (i.e., vectors)
    # (based on their Euclidean distance)
    # Note that it's k+1 because the source node will be included and later removed
    query_k = min(k + 1, num_nodes)
    neighbor_distances, nearest_neighbors = kdtree.query(
        theta[inv_node_map[source]], k=query_k
    )

    # Ensure results are always arrays (KDTree returns scalars when k=1)
    neighbor_distances = np.atleast_1d(neighbor_distances)
    nearest_neighbors = np.atleast_1d(nearest_neighbors)

    # The paper defines the similarity S(v_i, v_j) as
    # 1 / || Theta(v_i) - Theta(v_j) ||
    # Calculate reciprocals and normalize to [0, 1] range

    # Handle the case where distances are very small or zero (common in small graphs)
    # Use the passed in eps parameter instead of defining a new epsilon
    neighbor_distances = np.maximum(neighbor_distances, eps)
    similarities = 1 / neighbor_distances

    # Always normalize to ensure values are between 0 and 1
    if len(similarities) > 0 and (max_sim := np.max(similarities)) > 0:
        similarities /= max_sim

    # Add back the similarity scores (i.e., distances)
    # Convert numpy scalars to native Python types for dispatch compatibility
    top_k_with_val = dict(
        zip((node_list[n] for n in nearest_neighbors), similarities.tolist())
    )

    # Remove the self-similarity
    top_k_with_val.pop(source, None)

    # Ensure we return exactly k results (sorted by similarity)
    if len(top_k_with_val) > k:
        sorted_items = sorted(top_k_with_val.items(), key=lambda x: x[1], reverse=True)
        top_k_with_val = dict(sorted_items[:k])

    return top_k_with_val

