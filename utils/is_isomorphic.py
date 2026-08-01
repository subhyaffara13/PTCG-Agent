
def is_isomorphic(G, H):
    '''
    Check if the groups are isomorphic to each other

    Parameters
    ==========

    G : A finite ``FpGroup`` or a ``PermutationGroup``
        First group.

    H : A finite ``FpGroup`` or a ``PermutationGroup``
        Second group.

    Returns
    =======

    boolean
    '''
    return group_isomorphism(G, H, isomorphism=False)


def is_isomorphic(T1, T2):
    """
    Determine if two different cluster assignments are equivalent.

    Parameters
    ----------
    T1 : array_like
        An assignment of singleton cluster ids to flat cluster ids.
    T2 : array_like
        An assignment of singleton cluster ids to flat cluster ids.

    Returns
    -------
    b : bool
        Whether the flat cluster assignments `T1` and `T2` are
        equivalent.

    See Also
    --------
    linkage : for a description of what a linkage matrix is.
    fcluster : for the creation of flat cluster assignments.

    Examples
    --------
    >>> from scipy.cluster.hierarchy import fcluster, is_isomorphic
    >>> from scipy.cluster.hierarchy import single, complete
    >>> from scipy.spatial.distance import pdist

    Two flat cluster assignments can be isomorphic if they represent the same
    cluster assignment, with different labels.

    For example, we can use the `scipy.cluster.hierarchy.single` method
    and flatten the output to four clusters:

    >>> X = [[0, 0], [0, 1], [1, 0],
    ...      [0, 4], [0, 3], [1, 4],
    ...      [4, 0], [3, 0], [4, 1],
    ...      [4, 4], [3, 4], [4, 3]]

    >>> Z = single(pdist(X))
    >>> T = fcluster(Z, 1, criterion='distance')
    >>> T
    array([3, 3, 3, 4, 4, 4, 2, 2, 2, 1, 1, 1], dtype=int32)

    We can then do the same using the
    `scipy.cluster.hierarchy.complete`: method:

    >>> Z = complete(pdist(X))
    >>> T_ = fcluster(Z, 1.5, criterion='distance')
    >>> T_
    array([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4], dtype=int32)

    As we can see, in both cases we obtain four clusters and all the data
    points are distributed in the same way - the only thing that changes
    are the flat cluster labels (3 => 1, 4 =>2, 2 =>3 and 4 =>1), so both
    cluster assignments are isomorphic:

    >>> is_isomorphic(T, T_)
    True

    """
    xp = array_namespace(T1, T2)
    T1 = _asarray(T1, xp=xp)
    T2 = _asarray(T2, xp=xp)

    if T1.ndim != 1:
        raise ValueError('T1 must be one-dimensional.')
    if T2.ndim != 1:
        raise ValueError('T2 must be one-dimensional.')
    if T1.shape != T2.shape:
        raise ValueError('T1 and T2 must have the same number of elements.')

    # For each pair of (i, j) indices, test that
    # T1[i] == T1[j] <--> T2[i] == T2[j]
    # In other words, if the same symbol appears multiple times in T1,
    # then a potentially different symbol must also be repeated in the same
    # positions in T2, and vice versa.

    # O(n*log(n)) algorithm.
    # It is also possible to write a O(n) algorithm on top of unique_all(),
    # but in practice it's much slower even for large clusters.
    idx = xp.argsort(T1)
    T1 = xp.take(T1, idx)
    T2 = xp.take(T2, idx)
    changes1 = T1 != xp.roll(T1, -1)
    changes2 = T2 != xp.roll(T2, -1)
    return xp.all(changes1 == changes2)


def is_isomorphic(G1, G2, node_match=None, edge_match=None):
    """Returns True if the graphs G1 and G2 are isomorphic and False otherwise.

    Parameters
    ----------
    G1, G2: graphs
        The two graphs G1 and G2 must be the same type.

    node_match : callable
        A function that returns True if node n1 in G1 and n2 in G2 should
        be considered equal during the isomorphism test.
        If node_match is not specified then node attributes are not considered.

        The function will be called like

           node_match(G1.nodes[n1], G2.nodes[n2]).

        That is, the function will receive the node attribute dictionaries
        for n1 and n2 as inputs.

    edge_match : callable
        A function that returns True if the edge attribute dictionary
        for the pair of nodes (u1, v1) in G1 and (u2, v2) in G2 should
        be considered equal during the isomorphism test.  If edge_match is
        not specified then edge attributes are not considered.

        The function will be called like

           edge_match(G1[u1][v1], G2[u2][v2]).

        That is, the function will receive the edge attribute dictionaries
        of the edges under consideration.

    Notes
    -----
    Uses the vf2 algorithm [1]_.

    Examples
    --------
    >>> import networkx.algorithms.isomorphism as iso

    For digraphs G1 and G2, using 'weight' edge attribute (default: 1)

    >>> G1 = nx.DiGraph()
    >>> G2 = nx.DiGraph()
    >>> nx.add_path(G1, [1, 2, 3, 4], weight=1)
    >>> nx.add_path(G2, [10, 20, 30, 40], weight=2)
    >>> em = iso.numerical_edge_match("weight", 1)
    >>> nx.is_isomorphic(G1, G2)  # no weights considered
    True
    >>> nx.is_isomorphic(G1, G2, edge_match=em)  # match weights
    False

    For multidigraphs G1 and G2, using 'fill' node attribute (default: '')

    >>> G1 = nx.MultiDiGraph()
    >>> G2 = nx.MultiDiGraph()
    >>> G1.add_nodes_from([1, 2, 3], fill="red")
    >>> G2.add_nodes_from([10, 20, 30, 40], fill="red")
    >>> nx.add_path(G1, [1, 2, 3, 4], weight=3, linewidth=2.5)
    >>> nx.add_path(G2, [10, 20, 30, 40], weight=3)
    >>> nm = iso.categorical_node_match("fill", "red")
    >>> nx.is_isomorphic(G1, G2, node_match=nm)
    True

    For multidigraphs G1 and G2, using 'weight' edge attribute (default: 7)

    >>> G1.add_edge(1, 2, weight=7)
    1
    >>> G2.add_edge(10, 20)
    1
    >>> em = iso.numerical_multiedge_match("weight", 7, rtol=1e-6)
    >>> nx.is_isomorphic(G1, G2, edge_match=em)
    True

    For multigraphs G1 and G2, using 'weight' and 'linewidth' edge attributes
    with default values 7 and 2.5. Also using 'fill' node attribute with
    default value 'red'.

    >>> em = iso.numerical_multiedge_match(["weight", "linewidth"], [7, 2.5])
    >>> nm = iso.categorical_node_match("fill", "red")
    >>> nx.is_isomorphic(G1, G2, edge_match=em, node_match=nm)
    True

    See Also
    --------
    numerical_node_match, numerical_edge_match, numerical_multiedge_match
    categorical_node_match, categorical_edge_match, categorical_multiedge_match

    References
    ----------
    .. [1]  L. P. Cordella, P. Foggia, C. Sansone, M. Vento,
       "An Improved Algorithm for Matching Large Graphs",
       3rd IAPR-TC15 Workshop  on Graph-based Representations in
       Pattern Recognition, Cuen, pp. 149-159, 2001.
       https://www.researchgate.net/publication/200034365_An_Improved_Algorithm_for_Matching_Large_Graphs
    """
    if G1.is_directed() and G2.is_directed():
        GM = nx.algorithms.isomorphism.DiGraphMatcher
    elif (not G1.is_directed()) and (not G2.is_directed()):
        GM = nx.algorithms.isomorphism.GraphMatcher
    else:
        raise NetworkXError("Graphs G1 and G2 are not of the same type.")

    gm = GM(G1, G2, node_match=node_match, edge_match=edge_match)

    return gm.is_isomorphic()


def is_isomorphic(G, SG, edge_match=None, node_match=None):
    return iso.ISMAGS(G, SG, node_match, edge_match).is_isomorphic()

