
def degree_centrality(G, nodes):
    r"""Compute the degree centrality for nodes in a bipartite network.

    The degree centrality for a node `v` is the fraction of nodes
    connected to it.

    Parameters
    ----------
    G : graph
       A bipartite network

    nodes : list or container
      Container with all nodes in one bipartite node set.

    Returns
    -------
    centrality : dictionary
       Dictionary keyed by node with bipartite degree centrality as the value.

    Examples
    --------
    >>> G = nx.wheel_graph(5)
    >>> top_nodes = {0, 1, 2}
    >>> nx.bipartite.degree_centrality(G, nodes=top_nodes)
    {0: 2.0, 1: 1.5, 2: 1.5, 3: 1.0, 4: 1.0}

    See Also
    --------
    betweenness_centrality
    closeness_centrality
    :func:`~networkx.algorithms.bipartite.basic.sets`
    :func:`~networkx.algorithms.bipartite.basic.is_bipartite`

    Notes
    -----
    The nodes input parameter must contain all nodes in one bipartite node set,
    but the dictionary returned contains all nodes from both bipartite node
    sets. See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.

    For unipartite networks, the degree centrality values are
    normalized by dividing by the maximum possible degree (which is
    `n-1` where `n` is the number of nodes in G).

    In the bipartite case, the maximum possible degree of a node in a
    bipartite node set is the number of nodes in the opposite node set
    [1]_.  The degree centrality for a node `v` in the bipartite
    sets `U` with `n` nodes and `V` with `m` nodes is

    .. math::

        d_{v} = \frac{deg(v)}{m}, \mbox{for} v \in U ,

        d_{v} = \frac{deg(v)}{n}, \mbox{for} v \in V ,


    where `deg(v)` is the degree of node `v`.

    References
    ----------
    .. [1] Borgatti, S.P. and Halgin, D. In press. "Analyzing Affiliation
        Networks". In Carrington, P. and Scott, J. (eds) The Sage Handbook
        of Social Network Analysis. Sage Publications.
        https://dx.doi.org/10.4135/9781446294413.n28
    """
    top = set(nodes)
    bottom = set(G) - top
    s = 1.0 / len(bottom)
    centrality = {n: d * s for n, d in G.degree(top)}
    s = 1.0 / len(top)
    centrality.update({n: d * s for n, d in G.degree(bottom)})
    return centrality


def degree_centrality(G):
    """Compute the degree centrality for nodes.

    The degree centrality for a node v is the fraction of nodes it
    is connected to.

    Parameters
    ----------
    G : graph
      A networkx graph

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with degree centrality as the value.

    Examples
    --------
    >>> G = nx.Graph([(0, 1), (0, 2), (0, 3), (1, 2), (1, 3)])
    >>> nx.degree_centrality(G)
    {0: 1.0, 1: 1.0, 2: 0.6666666666666666, 3: 0.6666666666666666}

    See Also
    --------
    betweenness_centrality, load_centrality, eigenvector_centrality

    Notes
    -----
    The degree centrality values are normalized by dividing by the maximum
    possible degree in a simple graph n-1 where n is the number of nodes in G.

    For multigraphs or graphs with self loops the maximum degree might
    be higher than n-1 and values of degree centrality greater than 1
    are possible.
    """
    if len(G) <= 1:
        return {n: 1 for n in G}

    s = 1.0 / (len(G) - 1.0)
    centrality = {n: d * s for n, d in G.degree()}
    return centrality

