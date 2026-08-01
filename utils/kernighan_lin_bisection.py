
def kernighan_lin_bisection(G, partition=None, max_iter=10, weight="weight", seed=None):
    """Partition a graph into two blocks using the Kernighan–Lin algorithm.

    This algorithm partitions a network into two sets by iteratively
    swapping pairs of nodes to reduce the edge cut between the two sets.  The
    pairs are chosen according to a modified form of Kernighan-Lin [1]_, which
    moves nodes individually, alternating between sides to keep the bisection
    balanced.

    Kernighan-Lin is an approximate algorithm for maximal modularity bisection.
    In [2]_ they suggest that fine-tuned improvements can be made using
    greedy node swapping, (see `greedy_node_swap_bipartition`).
    The improvements are typically only a few percent of the modularity value.
    But they claim that can make a difference between a good and excellent method.
    This function does not perform any improvements. But you can do that yourself.

    Parameters
    ----------
    G : NetworkX graph
        Graph must be undirected.

    partition : tuple
        Pair of iterables containing an initial partition. If not
        specified, a random balanced partition is used.

    max_iter : int
        Maximum number of times to attempt swaps to find an
        improvement before giving up.

    weight : string or function (default: "weight")
        If this is a string, then edge weights will be accessed via the
        edge attribute with this key (that is, the weight of the edge
        joining `u` to `v` will be ``G.edges[u, v][weight]``). If no
        such edge attribute exists, the weight of the edge is assumed to
        be one.

        If this is a function, the weight of an edge is the value
        returned by the function. The function must accept exactly three
        positional arguments: the two endpoints of an edge and the
        dictionary of edge attributes for that edge. The function must
        return a number or None to indicate a hidden edge.

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.
        Only used if partition is None

    Returns
    -------
    partition : tuple
        A pair of sets of nodes representing the bipartition.

    Raises
    ------
    NetworkXError
        If `partition` is not a valid partition of the nodes of the graph.

    References
    ----------
    .. [1] Kernighan, B. W.; Lin, Shen (1970).
       "An efficient heuristic procedure for partitioning graphs."
       *Bell Systems Technical Journal* 49: 291--307.
       Oxford University Press 2011.
    .. [2] M. E. J. Newman,
       "Modularity and community structure in networks",
       PNAS, 103 (23), p. 8577-8582,
       https://doi.org/10.1073/pnas.0601602103

    """
    nodes = list(G)

    if partition is None:
        seed.shuffle(nodes)
        mid = len(nodes) // 2
        A, B = nodes[:mid], nodes[mid:]
    else:
        try:
            A, B = partition
        except (TypeError, ValueError) as err:
            raise nx.NetworkXError("partition must be two sets") from err
        if not nx.community.is_partition(G, [A, B]):
            raise nx.NetworkXError("partition invalid")

    side = {node: (node in A) for node in nodes}

    # ruff: noqa: E731   skips check for no lambda functions
    # Using shortest_paths _weight_function with sum instead of min on multiedges
    if callable(weight):
        sum_weight = weight
    elif G.is_multigraph():
        sum_weight = lambda u, v, d: sum(dd.get(weight, 1) for dd in d.values())
    else:
        sum_weight = lambda u, v, d: d.get(weight, 1)

    edge_info = {
        u: {v: wt for v, d in nbrs.items() if (wt := sum_weight(u, v, d)) is not None}
        for u, nbrs in G._adj.items()
    }

    for i in range(max_iter):
        costs = list(_kernighan_lin_sweep(edge_info, side))
        # find out how many edges to update: min_i
        min_cost, min_i, _ = min(costs)
        if min_cost >= 0:
            break

        for _, _, (u, v) in costs[:min_i]:
            side[u] = 1
            side[v] = 0

    part1 = {u for u, s in side.items() if s == 0}
    part2 = {u for u, s in side.items() if s == 1}
    return part1, part2

