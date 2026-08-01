
def configuration_model(deg_sequence, create_using=None, seed=None):
    """Returns a random graph with the given degree sequence.

    The configuration model generates a random pseudograph (graph with
    parallel edges and self loops) by randomly assigning edges to
    match the given degree sequence.

    Parameters
    ----------
    deg_sequence :  list of nonnegative integers
        Each list entry corresponds to the degree of a node.
    create_using : NetworkX graph constructor, optional (default MultiGraph)
        Graph type to create. If graph instance, then cleared before populated.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    Returns
    -------
    G : MultiGraph
        A graph with the specified degree sequence.
        Nodes are labeled starting at 0 with an index
        corresponding to the position in deg_sequence.

    Raises
    ------
    NetworkXError
        If the degree sequence does not have an even sum.

    See Also
    --------
    is_graphical

    Notes
    -----
    As described by Newman [1]_.

    A non-graphical degree sequence (not realizable by some simple
    graph) is allowed since this function returns graphs with self
    loops and parallel edges.  An exception is raised if the degree
    sequence does not have an even sum.

    This configuration model construction process can lead to
    duplicate edges and loops.  You can remove the self-loops and
    parallel edges (see below) which will likely result in a graph
    that doesn't have the exact degree sequence specified.

    The density of self-loops and parallel edges tends to decrease as
    the number of nodes increases. However, typically the number of
    self-loops will approach a Poisson distribution with a nonzero mean,
    and similarly for the number of parallel edges.  Consider a node
    with *k* stubs. The probability of being joined to another stub of
    the same node is basically (*k* - *1*) / *N*, where *k* is the
    degree and *N* is the number of nodes. So the probability of a
    self-loop scales like *c* / *N* for some constant *c*. As *N* grows,
    this means we expect *c* self-loops. Similarly for parallel edges.

    References
    ----------
    .. [1] M.E.J. Newman, "The structure and function of complex networks",
       SIAM REVIEW 45-2, pp 167-256, 2003.

    Examples
    --------
    You can create a degree sequence following a particular distribution
    by using the one of the distribution functions in
    :mod:`~networkx.utils.random_sequence` (or one of your own). For
    example, to create an undirected multigraph on one hundred nodes
    with degree sequence chosen from the power law distribution:

    >>> sequence = nx.random_powerlaw_tree_sequence(100, tries=5000)
    >>> G = nx.configuration_model(sequence)
    >>> len(G)
    100
    >>> actual_degrees = [d for v, d in G.degree()]
    >>> actual_degrees == sequence
    True

    The returned graph is a multigraph, which may have parallel
    edges. To remove any parallel edges from the returned graph:

    >>> G = nx.Graph(G)

    Similarly, to remove self-loops:

    >>> G.remove_edges_from(nx.selfloop_edges(G))

    """
    if sum(deg_sequence) % 2 != 0:
        msg = "Invalid degree sequence: sum of degrees must be even, not odd"
        raise nx.NetworkXError(msg)

    G = nx.empty_graph(0, create_using, default=nx.MultiGraph)
    if G.is_directed():
        raise nx.NetworkXNotImplemented("not implemented for directed graphs")

    G = _configuration_model(deg_sequence, G, seed=seed)

    return G


def configuration_model(aseq, bseq, create_using=None, seed=None):
    """Returns a random bipartite graph from two given degree sequences.

    Parameters
    ----------
    aseq : list
       Degree sequence for node set A.
    bseq : list
       Degree sequence for node set B.
    create_using : NetworkX graph instance, optional
       Return graph of this type.
    seed : integer, random_state, or None (default)
        Indicator of random number generation state.
        See :ref:`Randomness<randomness>`.

    The graph is composed of two partitions. Set A has nodes 0 to
    (len(aseq) - 1) and set B has nodes len(aseq) to (len(bseq) - 1).
    Nodes from set A are connected to nodes in set B by choosing
    randomly from the possible free stubs, one in A and one in B.

    Notes
    -----
    The sum of the two sequences must be equal: sum(aseq)=sum(bseq)
    If no graph type is specified use MultiGraph with parallel edges.
    If you want a graph with no parallel edges use create_using=Graph()
    but then the resulting degree sequences might not be exact.

    The nodes are assigned the attribute 'bipartite' with the value 0 or 1
    to indicate which bipartite set the node belongs to.

    This function is not imported in the main namespace.
    To use it use nx.bipartite.configuration_model
    """
    G = nx.empty_graph(0, create_using, default=nx.MultiGraph)
    if G.is_directed():
        raise nx.NetworkXError("Directed Graph not supported")

    # length and sum of each sequence
    lena = len(aseq)
    lenb = len(bseq)
    suma = sum(aseq)
    sumb = sum(bseq)

    if not suma == sumb:
        raise nx.NetworkXError(
            f"invalid degree sequences, sum(aseq)!=sum(bseq),{suma},{sumb}"
        )

    G = _add_nodes_with_bipartite_label(G, lena, lenb)

    if len(aseq) == 0 or max(aseq) == 0:
        return G  # done if no edges

    # build lists of degree-repeated vertex numbers
    stubs = [[v] * aseq[v] for v in range(lena)]
    astubs = [x for subseq in stubs for x in subseq]

    stubs = [[v] * bseq[v - lena] for v in range(lena, lena + lenb)]
    bstubs = [x for subseq in stubs for x in subseq]

    # shuffle lists
    seed.shuffle(astubs)
    seed.shuffle(bstubs)

    G.add_edges_from([astubs[i], bstubs[i]] for i in range(suma))

    G.name = "bipartite_configuration_model"
    return G

