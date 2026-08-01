
def kosaraju_strongly_connected_components(G, source=None):
    """Generate nodes in strongly connected components of graph.

    Parameters
    ----------
    G : NetworkX Graph
        A directed graph.

    source : node, optional (default=None)
        Specify a node from which to start the depth-first search.
        If not provided, the algorithm will start from an arbitrary node.

    Yields
    ------
    set
        A set of all nodes in a strongly connected component of `G`.

    Raises
    ------
    NetworkXNotImplemented
        If `G` is undirected.

    NetworkXError
        If `source` is not a node in `G`.

    Examples
    --------
    Generate a list of strongly connected components of a graph:

    >>> G = nx.cycle_graph(4, create_using=nx.DiGraph())
    >>> nx.add_cycle(G, [10, 11, 12])
    >>> sorted(nx.kosaraju_strongly_connected_components(G), key=len, reverse=True)
    [{0, 1, 2, 3}, {10, 11, 12}]

    If you only want the largest component, it's more efficient to
    use `max()` instead of `sorted()`.

    >>> max(nx.kosaraju_strongly_connected_components(G), key=len)
    {0, 1, 2, 3}

    See Also
    --------
    strongly_connected_components

    Notes
    -----
    Uses Kosaraju's algorithm.
    """
    post = list(nx.dfs_postorder_nodes(G.reverse(copy=False), source=source))
    n = len(post)
    seen = set()
    while post and len(seen) < n:
        r = post.pop()
        if r in seen:
            continue
        new = {r}
        seen.add(r)
        stack = [r]
        while stack and len(seen) < n:
            v = stack.pop()
            for w in G._adj[v]:
                if w not in seen:
                    new.add(w)
                    seen.add(w)
                    stack.append(w)
        yield new

