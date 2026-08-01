
def is_regular(G):
    """Determines whether a graph is regular.

    A regular graph is a graph where all nodes have the same degree. A regular
    digraph is a graph where all nodes have the same indegree and all nodes
    have the same outdegree.

    Parameters
    ----------
    G : NetworkX graph

    Returns
    -------
    bool
        Whether the given graph or digraph is regular.

    Examples
    --------
    >>> G = nx.DiGraph([(1, 2), (2, 3), (3, 4), (4, 1)])
    >>> nx.is_regular(G)
    True

    """
    if len(G) == 0:
        raise nx.NetworkXPointlessConcept("Graph has no nodes.")
    n1 = nx.utils.arbitrary_element(G)
    if not G.is_directed():
        d1 = G.degree(n1)
        return all(d1 == d for _, d in G.degree)
    else:
        d_in = G.in_degree(n1)
        in_regular = (d_in == d for _, d in G.in_degree)
        d_out = G.out_degree(n1)
        out_regular = (d_out == d for _, d in G.out_degree)
        return all(in_regular) and all(out_regular)

