
def connected_components(G):
    r"""
    Connected components of an undirected graph or weakly connected components
    of a directed graph.


    Parameters
    ==========

    G : tuple[list, list[tuple[T, T]]
        A tuple consisting of a list of vertices and a list of edges of
        a graph whose connected components are to be found.


    Examples
    ========


    Given an undirected graph::

        graph {
            A -- B
            C -- D
        }

    .. graphviz::

        graph {
            A -- B
            C -- D
        }

    We can find the connected components using this function if we include
    each edge in both directions::

        >>> from sympy.utilities.iterables import connected_components

        >>> V = ['A', 'B', 'C', 'D']
        >>> E = [('A', 'B'), ('B', 'A'), ('C', 'D'), ('D', 'C')]
        >>> connected_components((V, E))
        [['A', 'B'], ['C', 'D']]

    The weakly connected components of a directed graph can found the same
    way.


    Notes
    =====

    The vertices of the graph must be hashable for the data structures used.
    If the vertices are unhashable replace them with integer indices.

    This function uses Tarjan's algorithm to compute the connected components
    in `O(|V|+|E|)` (linear) time.


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Component_%28graph_theory%29
    .. [2] https://en.wikipedia.org/wiki/Tarjan%27s_strongly_connected_components_algorithm


    See Also
    ========

    sympy.utilities.iterables.strongly_connected_components

    """
    # Duplicate edges both ways so that the graph is effectively undirected
    # and return the strongly connected components:
    V, E = G
    E_undirected = []
    for v1, v2 in E:
        E_undirected.extend([(v1, v2), (v2, v1)])
    return strongly_connected_components((V, E_undirected))


def connected_components(G):
    """Generate connected components.

    The connected components of an undirected graph partition the graph into
    disjoint sets of nodes. Each of these sets induces a subgraph of graph
    `G` that is connected and not part of any larger connected subgraph.

    A graph is connected (:func:`is_connected`) if, for every pair of distinct
    nodes, there is a path between them. If there is a pair of nodes for
    which such path does not exist, the graph is not connected (also referred
    to as "disconnected").

    A graph consisting of a single node and no edges is connected.
    Connectivity is undefined for the null graph (graph with no nodes).

    Parameters
    ----------
    G : NetworkX graph
       An undirected graph

    Yields
    ------
    comp : set
       A set of nodes in one connected component of the graph.

    Raises
    ------
    NetworkXNotImplemented
        If G is directed.

    Examples
    --------
    Generate a sorted list of connected components, largest first.

    >>> G = nx.path_graph(4)
    >>> nx.add_path(G, [10, 11, 12])
    >>> [len(c) for c in sorted(nx.connected_components(G), key=len, reverse=True)]
    [4, 3]

    If you only want the largest connected component, it's more
    efficient to use max instead of sort.

    >>> largest_cc = max(nx.connected_components(G), key=len)

    To create the induced subgraph of each component use:

    >>> S = [G.subgraph(c).copy() for c in nx.connected_components(G)]

    See Also
    --------
    number_connected_components
    is_connected
    number_weakly_connected_components
    number_strongly_connected_components

    Notes
    -----
    This function is for undirected graphs only. For directed graphs, use
    :func:`strongly_connected_components` or
    :func:`weakly_connected_components`.

    The algorithm is based on a Breadth-First Search (BFS) traversal and its
    time complexity is $O(n + m)$, where $n$ is the number of nodes and $m$ the
    number of edges in the graph.

    """
    seen = set()
    n = len(G)  # must be outside the loop to avoid performance hit with graph views
    for v in G:
        if v not in seen:
            c = _plain_bfs(G, n - len(seen), v)
            seen.update(c)
            yield c

