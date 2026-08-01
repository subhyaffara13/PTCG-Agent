
def hamiltonian_path(G):
    """Returns a Hamiltonian path in the given tournament graph.

    Each tournament has a Hamiltonian path. If furthermore, the
    tournament is strongly connected, then the returned Hamiltonian path
    is a Hamiltonian cycle (by joining the endpoints of the path).

    Parameters
    ----------
    G : NetworkX graph
        A directed graph representing a tournament.

    Returns
    -------
    path : list
        A list of nodes which form a Hamiltonian path in `G`.

    Examples
    --------
    >>> G = nx.DiGraph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
    >>> nx.is_tournament(G)
    True
    >>> nx.tournament.hamiltonian_path(G)
    [0, 1, 2, 3]

    Notes
    -----
    This is a recursive implementation with an asymptotic running time
    of $O(n^2)$, ignoring multiplicative polylogarithmic factors, where
    $n$ is the number of nodes in the graph.

    """
    if len(G) == 0:
        return []
    if len(G) == 1:
        return [arbitrary_element(G)]
    v = arbitrary_element(G)
    hampath = hamiltonian_path(G.subgraph(set(G) - {v}))
    # Get the index of the first node in the path that does *not* have
    # an edge to `v`, then insert `v` before that node.
    index = index_satisfying(hampath, lambda u: v not in G[u])
    hampath.insert(index, v)
    return hampath


def hamiltonian_path(G, source):
    source = arbitrary_element(G)
    neighbors = set(G[source]) - {source}
    n = len(G)
    for target in neighbors:
        for path in nx.all_simple_paths(G, source, target):
            if len(path) == n:
                yield path

