
def descendants(G, source):
    """Returns all nodes reachable from `source` in `G`.

    Parameters
    ----------
    G : NetworkX Graph
    source : node in `G`

    Returns
    -------
    set()
        The descendants of `source` in `G`

    Raises
    ------
    NetworkXError
        If node `source` is not in `G`.

    Examples
    --------
    >>> DG = nx.path_graph(5, create_using=nx.DiGraph)
    >>> sorted(nx.descendants(DG, 2))
    [3, 4]

    The `source` node is not a descendant of itself, but can be included manually:

    >>> sorted(nx.descendants(DG, 2) | {2})
    [2, 3, 4]

    See also
    --------
    ancestors
    """
    return {child for parent, child in nx.bfs_edges(G, source)}

