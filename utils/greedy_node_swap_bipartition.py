import random

def greedy_node_swap_bipartition(G, *, init_split=None, max_iter=10):
    """Split the nodes into two communities based on greedy
    modularity maximization.

    The algorithm works by selecting a node to change communities which
    will maximize the modularity. The swap is made and the community
    structure with the highest modularity is kept.

    Parameters
    ----------
    G : NetworkX graph

    init_split : 2-tuple of sets of nodes
        Pair of sets of nodes in ``G`` providing an initial bipartition
        for the algorithm. If not specified, a random balanced partition
        is used. If this pair of sets is not a partition of the nodes of `G`,
        :exc:`NetworkXException` is raised.

    max_iter : int
      Maximum number of iterations of attempting swaps to find an improvement.

    Returns
    -------
    max_split : 2-tuple of sets of nodes
        Pair of sets of nodes of ``G``, partitioned according to a
        node swap greedy modularity maximization algorithm.

    Raises
    ------
    NetworkXError
      if init_split is not a valid partition of the
      graph into two communities or if G is a MultiGraph

    Examples
    --------
    >>> G = nx.barbell_graph(3, 0)
    >>> left, right = nx.community.greedy_node_swap_bipartition(G)
    >>> # Sort the communities so the nodes appear in increasing order.
    >>> left, right = sorted([sorted(left), sorted(right)])
    >>> sorted(left)
    [0, 1, 2]
    >>> sorted(right)
    [3, 4, 5]

    Notes
    -----
    This function is not implemented for multigraphs.

    References
    ----------
    .. [1] M. E. J. Newman "Networks: An Introduction", pages 373--375.
       Oxford University Press 2011.

    """
    if init_split is None:
        m1 = len(G) // 2
        m2 = len(G) - m1
        some_nodes = set(random.sample(list(G), m1))
        other_nodes = {n for n in G if n not in some_nodes}
        best_split_so_far = (some_nodes, other_nodes)
    else:
        if not nx.community.is_partition(G, init_split):
            raise nx.NetworkXError("init_split is not a partition of G")
        if not len(init_split) == 2:
            raise nx.NetworkXError("init_split must be a bipartition")
        best_split_so_far = deepcopy(init_split)

    best_mod = nx.community.modularity(G, best_split_so_far)

    max_split, max_mod = best_split_so_far, best_mod
    its = 0
    m = G.number_of_edges()
    G_degree = dict(G.degree)

    while max_mod >= best_mod and its < max_iter:
        best_split_so_far = max_split
        best_mod = max_mod
        next_split = deepcopy(max_split)
        next_mod = max_mod
        nodes = set(G)
        while nodes:
            max_swap = -1
            max_node = None
            max_node_comm = None
            left, right = next_split
            leftd = sum(G_degree[n] for n in left)
            rightd = sum(G_degree[n] for n in right)
            for n in nodes:
                if n in left:
                    in_comm, out_comm = left, right
                    in_deg, out_deg = leftd, rightd
                else:
                    in_comm, out_comm = right, left
                    in_deg, out_deg = rightd, leftd

                d_eii = -len(G[n].keys() & in_comm) / m
                d_ejj = len(G[n].keys() & out_comm) / m
                deg = G_degree[n]
                d_sum_ai = (deg / (2 * m**2)) * (in_deg - out_deg - deg)
                swap_change = d_eii + d_ejj + d_sum_ai

                if swap_change > max_swap:
                    max_swap = swap_change
                    max_node = n
                    max_node_comm = in_comm
                    non_max_node_comm = out_comm
            # swap the node from one comm to the other
            max_node_comm.remove(max_node)
            non_max_node_comm.add(max_node)
            next_mod += max_swap
            # deepcopy next_split each time it reaches a high (might go lower later)
            if next_mod > max_mod:
                max_split, max_mod = deepcopy(next_split), next_mod
            nodes.remove(max_node)
        its += 1
    return best_split_so_far

