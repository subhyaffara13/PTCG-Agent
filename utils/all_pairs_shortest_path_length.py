
def all_pairs_shortest_path_length(G, cutoff=None):
    """Computes the shortest path lengths between all nodes in `G`.

    Parameters
    ----------
    G : NetworkX graph

    cutoff : integer, optional
        Depth at which to stop the search. Only paths of length at most
        `cutoff` (i.e. paths containing <= ``cutoff + 1`` nodes) are returned.

    Returns
    -------
    lengths : iterator
        (source, dictionary) iterator with dictionary keyed by target and
        shortest path length as the key value.

    Notes
    -----
    The iterator returned only has reachable node pairs.

    Examples
    --------
    >>> G = nx.path_graph(5)
    >>> length = dict(nx.all_pairs_shortest_path_length(G))
    >>> for node in [0, 1, 2, 3, 4]:
    ...     print(f"1 - {node}: {length[1][node]}")
    1 - 0: 1
    1 - 1: 0
    1 - 2: 1
    1 - 3: 2
    1 - 4: 3
    >>> length[3][2]
    1
    >>> length[2][2]
    0

    Only include paths with length less than or equal to the `cutoff` keyword
    argument:

    >>> path_lengths = dict(nx.all_pairs_shortest_path_length(G, cutoff=2))
    >>> path_lengths[1]  # node 4 is too far away to appear
    {1: 0, 0: 1, 2: 1, 3: 2}
    """
    length = single_source_shortest_path_length
    # TODO This can be trivially parallelized.
    for n in G:
        yield (n, length(G, n, cutoff=cutoff))

