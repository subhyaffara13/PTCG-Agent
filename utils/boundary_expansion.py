
def boundary_expansion(G, S):
    """Returns the boundary expansion of the set `S`.

    The *boundary expansion* of a set `S` is the ratio between the size of its
    node boundary and the cardinality of the set itself [1]_ .

    Parameters
    ----------
    G : NetworkX graph
        The input graph.

    S : collection
        A collection of nodes in `G`.

    Returns
    -------
    number
        The boundary expansion ratio: size of node boundary / size of `S`.

    Examples
    --------
    The node boundary is {2, 3} (size 2), divided by ``|S|=2``:

    >>> G = nx.cycle_graph(4)
    >>> S = {0, 1}
    >>> nx.boundary_expansion(G, S)
    1.0

    For disconnected sets, e.g. here where the node boundary is ``{1, 3, 5}``:

    >>> G = nx.cycle_graph(6)
    >>> S = {0, 2, 4}
    >>> nx.boundary_expansion(G, S)
    1.0

    See also
    --------
    :func:`~networkx.algorithms.boundary.node_boundary`
    edge_expansion
    mixing_expansion
    node_expansion

    Notes
    -----
    The node boundary is defined as all nodes not in `S` that are adjacent to
    nodes in `S`.

    References
    ----------
    .. [1] Vadhan, Salil P.
       "Pseudorandomness." *Foundations and Trends in Theoretical Computer Science*
       7.1–3 (2011): 1–336. <https://doi.org/10.1561/0400000010>
    """
    return len(nx.node_boundary(G, S)) / len(S)

