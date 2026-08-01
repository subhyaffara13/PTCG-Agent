
def all_simple_edge_paths(G, source, target, cutoff=None):
    """Generate lists of edges for all simple paths in G from source to target.

    A simple path is a path with no repeated nodes.

    Parameters
    ----------
    G : NetworkX graph

    source : node
       Starting node for path

    target : nodes
       Single node or iterable of nodes at which to end path

    cutoff : integer, optional
        Depth to stop the search. Only paths with length <= `cutoff` are returned.
        Note that the length of an edge path is the number of edges.

    Returns
    -------
    path_generator: generator
       A generator that produces lists of simple paths.  If there are no paths
       between the source and target within the given cutoff the generator
       produces no output.
       For multigraphs, the list of edges have elements of the form `(u,v,k)`.
       Where `k` corresponds to the edge key.

    Examples
    --------

    Print the simple path edges of a Graph::

        >>> g = nx.Graph([(1, 2), (2, 4), (1, 3), (3, 4)])
        >>> for path in sorted(nx.all_simple_edge_paths(g, 1, 4)):
        ...     print(path)
        [(1, 2), (2, 4)]
        [(1, 3), (3, 4)]

    Print the simple path edges of a MultiGraph. Returned edges come with
    their associated keys::

        >>> mg = nx.MultiGraph()
        >>> mg.add_edge(1, 2, key="k0")
        'k0'
        >>> mg.add_edge(1, 2, key="k1")
        'k1'
        >>> mg.add_edge(2, 3, key="k0")
        'k0'
        >>> for path in sorted(nx.all_simple_edge_paths(mg, 1, 3)):
        ...     print(path)
        [(1, 2, 'k0'), (2, 3, 'k0')]
        [(1, 2, 'k1'), (2, 3, 'k0')]

    When ``source`` is one of the targets, the empty path starting and ending at
    ``source`` without traversing any edge is considered a valid simple edge path
    and is included in the results:

        >>> G = nx.Graph()
        >>> G.add_node(0)
        >>> paths = list(nx.all_simple_edge_paths(G, 0, 0))
        >>> for path in paths:
        ...     print(path)
        []
        >>> len(paths)
        1

    You can use the `cutoff` parameter to only generate paths that are
    shorter than a certain length:

        >>> g = nx.Graph([(1, 2), (2, 3), (3, 4), (4, 5), (1, 4), (1, 5)])
        >>> for path in sorted(nx.all_simple_edge_paths(g, 1, 5)):
        ...     print(path)
        [(1, 2), (2, 3), (3, 4), (4, 5)]
        [(1, 4), (4, 5)]
        [(1, 5)]
        >>> for path in sorted(nx.all_simple_edge_paths(g, 1, 5, cutoff=1)):
        ...     print(path)
        [(1, 5)]
        >>> for path in sorted(nx.all_simple_edge_paths(g, 1, 5, cutoff=2)):
        ...     print(path)
        [(1, 4), (4, 5)]
        [(1, 5)]

    Notes
    -----
    This algorithm uses a modified depth-first search to generate the
    paths [1]_.  A single path can be found in $O(V+E)$ time but the
    number of simple paths in a graph can be very large, e.g. $O(n!)$ in
    the complete graph of order $n$.

    References
    ----------
    .. [1] R. Sedgewick, "Algorithms in C, Part 5: Graph Algorithms",
       Addison Wesley Professional, 3rd ed., 2001.

    See Also
    --------
    all_shortest_paths, shortest_path, all_simple_paths

    """
    if source not in G:
        raise nx.NodeNotFound(f"source node {source} not in graph")

    if target in G:
        targets = {target}
    else:
        try:
            targets = set(target)
        except TypeError as err:
            raise nx.NodeNotFound(f"target node {target} not in graph") from err

    cutoff = cutoff if cutoff is not None else len(G) - 1

    if cutoff >= 0 and targets:
        yield from _all_simple_edge_paths(G, source, targets, cutoff)

