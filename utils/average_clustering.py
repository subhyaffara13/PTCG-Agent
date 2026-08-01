
def average_clustering(G, nodes=None, weight=None, count_zeros=True):
    r"""Compute the average clustering coefficient for the graph G.

    The clustering coefficient for the graph is the average,

    .. math::

       C = \frac{1}{n}\sum_{v \in G} c_v,

    where :math:`n` is the number of nodes in `G`.

    Parameters
    ----------
    G : graph

    nodes : container of nodes, optional (default=all nodes in G)
       Compute average clustering for nodes in this container.

    weight : string or None, optional (default=None)
       The edge attribute that holds the numerical value used as a weight.
       If None, then each edge has weight 1.

    count_zeros : bool
       If False include only the nodes with nonzero clustering in the average.

    Returns
    -------
    avg : float
       Average clustering

    Examples
    --------
    >>> G = nx.complete_graph(5)
    >>> print(nx.average_clustering(G))
    1.0

    Notes
    -----
    This is a space saving routine; it might be faster
    to use the clustering function to get a list and then take the average.

    Self loops are ignored.

    References
    ----------
    .. [1] Generalizations of the clustering coefficient to weighted
       complex networks by J. Saramäki, M. Kivelä, J.-P. Onnela,
       K. Kaski, and J. Kertész, Physical Review E, 75 027105 (2007).
       http://jponnela.com/web_documents/a9.pdf
    .. [2] Marcus Kaiser,  Mean clustering coefficients: the role of isolated
       nodes and leafs on clustering measures for small-world networks.
       https://arxiv.org/abs/0802.2512
    """
    c = clustering(G, nodes, weight=weight).values()
    if not count_zeros:
        c = [v for v in c if abs(v) > 0]
    return sum(c) / len(c)


def average_clustering(G, trials=1000, seed=None):
    r"""Estimates the average clustering coefficient of G.

    The local clustering of each node in `G` is the fraction of triangles
    that actually exist over all possible triangles in its neighborhood.
    The average clustering coefficient of a graph `G` is the mean of
    local clusterings.

    This function finds an approximate average clustering coefficient
    for G by repeating `n` times (defined in `trials`) the following
    experiment: choose a node at random, choose two of its neighbors
    at random, and check if they are connected. The approximate
    coefficient is the fraction of triangles found over the number
    of trials [1]_.

    Parameters
    ----------
    G : NetworkX graph

    trials : integer
        Number of trials to perform (default 1000).

    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    c : float
        Approximated average clustering coefficient.

    Examples
    --------
    >>> from networkx.algorithms import approximation
    >>> G = nx.erdos_renyi_graph(10, 0.2, seed=10)
    >>> approximation.average_clustering(G, trials=1000, seed=10)
    0.214

    Raises
    ------
    NetworkXNotImplemented
        If G is directed.

    References
    ----------
    .. [1] Schank, Thomas, and Dorothea Wagner. Approximating clustering
       coefficient and transitivity. Universität Karlsruhe, Fakultät für
       Informatik, 2004.
       https://doi.org/10.5445/IR/1000001239

    """
    n = len(G)
    triangles = 0
    nodes = list(G)
    for i in [int(seed.random() * n) for i in range(trials)]:
        nbrs = list(G[nodes[i]])
        if len(nbrs) < 2:
            continue
        u, v = seed.sample(nbrs, 2)
        if u in G[v]:
            triangles += 1
    return triangles / trials


def average_clustering(G, nodes=None, mode="dot"):
    r"""Compute the average bipartite clustering coefficient.

    A clustering coefficient for the whole graph is the average,

    .. math::

       C = \frac{1}{n}\sum_{v \in G} c_v,

    where `n` is the number of nodes in `G`.

    Similar measures for the two bipartite sets can be defined [1]_

    .. math::

       C_X = \frac{1}{|X|}\sum_{v \in X} c_v,

    where `X` is a bipartite set of `G`.

    Parameters
    ----------
    G : graph
        a bipartite graph

    nodes : list or iterable, optional
        A container of nodes to use in computing the average.
        The nodes should be either the entire graph (the default) or one of the
        bipartite sets.

    mode : string
        The pairwise bipartite clustering method.
        It must be "dot", "max", or "min"

    Returns
    -------
    clustering : float
       The average bipartite clustering for the given set of nodes or the
       entire graph if no nodes are specified.

    Examples
    --------
    >>> from networkx.algorithms import bipartite
    >>> G = nx.star_graph(3)  # star graphs are bipartite
    >>> bipartite.average_clustering(G)
    0.75
    >>> X, Y = bipartite.sets(G)
    >>> bipartite.average_clustering(G, X)
    0.0
    >>> bipartite.average_clustering(G, Y)
    1.0

    See Also
    --------
    clustering

    Notes
    -----
    The container of nodes passed to this function must contain all of the nodes
    in one of the bipartite sets ("top" or "bottom") in order to compute
    the correct average bipartite clustering coefficients.
    See :mod:`bipartite documentation <networkx.algorithms.bipartite>`
    for further details on how bipartite graphs are handled in NetworkX.


    References
    ----------
    .. [1] Latapy, Matthieu, Clémence Magnien, and Nathalie Del Vecchio (2008).
        Basic notions for the analysis of large two-mode networks.
        Social Networks 30(1), 31--48.
    """
    if nodes is None:
        nodes = G
    ccs = latapy_clustering(G, nodes=nodes, mode=mode)
    return sum(ccs[v] for v in nodes) / len(nodes)

