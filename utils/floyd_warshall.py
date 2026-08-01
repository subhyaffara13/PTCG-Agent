
def floyd_warshall(G, weight="weight"):
    """Find all-pairs shortest path lengths using Floyd's algorithm.

    Parameters
    ----------
    G : NetworkX graph

    weight: string, optional (default= 'weight')
       Edge data key corresponding to the edge weight.


    Returns
    -------
    distance : dict
       A dictionary,  keyed by source and target, of shortest paths distances
       between nodes.

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.DiGraph()
    >>> G.add_weighted_edges_from(
    ...     [(0, 1, 5), (1, 2, 2), (2, 3, -3), (1, 3, 10), (3, 2, 8)]
    ... )
    >>> fw = nx.floyd_warshall(G, weight="weight")
    >>> results = {a: dict(b) for a, b in fw.items()}
    >>> pprint(results)
    {0: {0: 0, 1: 5, 2: 7, 3: 4},
     1: {0: inf, 1: 0, 2: 2, 3: -1},
     2: {0: inf, 1: inf, 2: 0, 3: -3},
     3: {0: inf, 1: inf, 2: 8, 3: 0}}

    Notes
    -----
    Floyd's algorithm is appropriate for finding shortest paths
    in dense graphs or graphs with negative weights when Dijkstra's algorithm
    fails.  This algorithm can still fail if there are negative cycles.
    It has running time $O(n^3)$ with running space of $O(n^2)$.

    See Also
    --------
    floyd_warshall_predecessor_and_distance
    floyd_warshall_numpy
    all_pairs_shortest_path
    all_pairs_shortest_path_length
    """
    # could make this its own function to reduce memory costs
    return floyd_warshall_predecessor_and_distance(G, weight=weight)[1]

