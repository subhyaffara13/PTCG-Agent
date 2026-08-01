
def panther_similarity(
    G,
    source,
    k=5,
    path_length=5,
    c=0.5,
    delta=0.1,
    eps=None,
    weight="weight",
    seed=None,
):
    r"""Returns the Panther similarity of nodes in the graph `G` to node ``v``.

    Panther is a similarity metric that says "two objects are considered
    to be similar if they frequently appear on the same paths." [1]_.

    Parameters
    ----------
    G : NetworkX graph
        A NetworkX graph
    source : node
        Source node for which to find the top `k` similar other nodes
    k : int (default = 5)
        The number of most similar nodes to return.
    path_length : int (default = 5)
        How long the randomly generated paths should be (``T`` in [1]_)
    c : float (default = 0.5)
        A universal constant that controls the number of random paths to generate.
        Higher values increase the number of sample paths and potentially improve
        accuracy at the cost of more computation. Defaults to 0.5 as recommended
        in [1]_.
    delta : float (default = 0.1)
        The probability that the similarity $S$ is not an epsilon-approximation to (R, phi),
        where $R$ is the number of random paths and $\phi$ is the probability
        that an element sampled from a set $A \subseteq D$, where $D$ is the domain.
    eps : float or None (default = None)
        The error bound for similarity approximation. This controls the accuracy
        of the sampled paths in representing the true similarity. Smaller values
        yield more accurate results but require more sample paths. If `None`, a
        value of ``sqrt(1/|E|)`` is used, which the authors found empirically
        effective.
    weight : string or None, optional (default="weight")
        The name of an edge attribute that holds the numerical value
        used as a weight. If None then each edge has weight 1.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    similarity : dictionary
        Dictionary of nodes to similarity scores (as floats). Note:
        the self-similarity (i.e., ``v``) will not be included in
        the returned dictionary. So, for ``k = 5``, a dictionary of
        top 4 nodes and their similarity scores will be returned.

    Raises
    ------
    NetworkXUnfeasible
        If `source` is an isolated node.

    NodeNotFound
        If `source` is not in `G`.

    Notes
    -----
        The isolated nodes in `G` are ignored.

    Examples
    --------
    >>> G = nx.star_graph(10)
    >>> sim = nx.panther_similarity(G, 0)

    References
    ----------
    .. [1] Zhang, J., Tang, J., Ma, C., Tong, H., Jing, Y., & Li, J.
           Panther: Fast top-k similarity search on large networks.
           In Proceedings of the ACM SIGKDD International Conference
           on Knowledge Discovery and Data Mining (Vol. 2015-August, pp. 1445–1454).
           Association for Computing Machinery. https://doi.org/10.1145/2783258.2783267.
    """
    import numpy as np

    # Use helper method to prepare common data structures
    G, inv_node_map, index_map, inv_sample_size, eps = _prepare_panther_paths(
        G,
        source,
        path_length=path_length,
        c=c,
        delta=delta,
        eps=eps,
        weight=weight,
        k=k,
        seed=seed,
    )

    num_nodes = G.number_of_nodes()
    node_list = list(G.nodes)

    # Check number of nodes after any modifications by _prepare_panther_paths
    if num_nodes < k:
        raise nx.NetworkXUnfeasible(
            f"The number of requested nodes {k} is greater than the number of nodes {num_nodes}."
        )

    S = np.zeros(num_nodes)
    source_paths = set(index_map[source])

    # Calculate the path similarities
    # between ``source`` (v) and ``node`` (v_j)
    # using our inverted index mapping of
    # vertices to paths
    for node, paths in index_map.items():
        # Only consider paths where both
        # ``node`` and ``source`` are present
        common_paths = source_paths.intersection(paths)
        S[inv_node_map[node]] = len(common_paths) * inv_sample_size

    # Retrieve top ``k+1`` similar to account for removing self-similarity
    # Note: the below performed anywhere from 4-10x faster
    # (depending on input sizes) vs the equivalent ``np.argsort(S)[::-1]``
    partition_k = min(k + 1, num_nodes)
    top_k_unsorted = np.argpartition(S, -partition_k)[-partition_k:]
    top_k_sorted = top_k_unsorted[np.argsort(S[top_k_unsorted])][::-1]

    # Add back the similarity scores
    # Convert numpy scalars to native Python types for dispatch compatibility
    top_k_with_val = dict(
        zip((node_list[i] for i in top_k_sorted), S[top_k_sorted].tolist())
    )

    # Remove the self-similarity
    top_k_with_val.pop(source, None)
    return top_k_with_val

