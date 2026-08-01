
def havel_hakimi_graph(deg_sequence, create_using=None):
    """Returns a simple graph with given degree sequence constructed
    using the Havel-Hakimi algorithm.

    Parameters
    ----------
    deg_sequence: list of integers
        Each integer corresponds to the degree of a node (need not be sorted).
    create_using : NetworkX graph constructor, optional (default=nx.Graph)
        Graph type to create. If graph instance, then cleared before populated.
        Directed graphs are not allowed.

    Raises
    ------
    NetworkXException
        For a non-graphical degree sequence (i.e. one
        not realizable by some simple graph).

    Notes
    -----
    The Havel-Hakimi algorithm constructs a simple graph by
    successively connecting the node of highest degree to other nodes
    of highest degree, resorting remaining nodes by degree, and
    repeating the process. The resulting graph has a high
    degree-associativity.  Nodes are labeled 1,.., len(deg_sequence),
    corresponding to their position in deg_sequence.

    The basic algorithm is from Hakimi [1]_ and was generalized by
    Kleitman and Wang [2]_.

    References
    ----------
    .. [1] Hakimi S., On Realizability of a Set of Integers as
       Degrees of the Vertices of a Linear Graph. I,
       Journal of SIAM, 10(3), pp. 496-506 (1962)
    .. [2] Kleitman D.J. and Wang D.L.
       Algorithms for Constructing Graphs and Digraphs with Given Valences
       and Factors  Discrete Mathematics, 6(1), pp. 79-88 (1973)
    """
    if not nx.is_graphical(deg_sequence):
        raise nx.NetworkXError("Invalid degree sequence")

    p = len(deg_sequence)
    G = nx.empty_graph(p, create_using)
    if G.is_directed():
        raise nx.NetworkXError("Directed graphs are not supported")
    num_degs = [[] for i in range(p)]
    dmax, dsum, n = 0, 0, 0
    for d in deg_sequence:
        # Process only the non-zero integers
        if d > 0:
            num_degs[d].append(n)
            dmax, dsum, n = max(dmax, d), dsum + d, n + 1
    # Return graph if no edges
    if n == 0:
        return G

    modstubs = [(0, 0)] * (dmax + 1)
    # Successively reduce degree sequence by removing the maximum degree
    while n > 0:
        # Retrieve the maximum degree in the sequence
        while len(num_degs[dmax]) == 0:
            dmax -= 1
        # If there are not enough stubs to connect to, then the sequence is
        # not graphical
        if dmax > n - 1:
            raise nx.NetworkXError("Non-graphical integer sequence")

        # Remove largest stub in list
        source = num_degs[dmax].pop()
        n -= 1
        # Reduce the next dmax largest stubs
        mslen = 0
        k = dmax
        for i in range(dmax):
            while len(num_degs[k]) == 0:
                k -= 1
            target = num_degs[k].pop()
            G.add_edge(source, target)
            n -= 1
            if k > 1:
                modstubs[mslen] = (k - 1, target)
                mslen += 1
        # Add back to the list any nonzero stubs that were removed
        for i in range(mslen):
            (stubval, stubtarget) = modstubs[i]
            num_degs[stubval].append(stubtarget)
            n += 1

    return G


def havel_hakimi_graph(aseq, bseq, create_using=None):
    """Returns a bipartite graph from two given degree sequences using a
    Havel-Hakimi style construction.

    The graph is composed of two partitions. Set A has nodes 0 to
    (len(aseq) - 1) and set B has nodes len(aseq) to (len(bseq) - 1).
    Nodes from the set A are connected to nodes in the set B by
    connecting the highest degree nodes in set A to the highest degree
    nodes in set B until all stubs are connected.

    Parameters
    ----------
    aseq : list
       Degree sequence for node set A.
    bseq : list
       Degree sequence for node set B.
    create_using : NetworkX graph instance, optional
       Return graph of this type.

    Notes
    -----
    The sum of the two sequences must be equal: sum(aseq)=sum(bseq)
    If no graph type is specified use MultiGraph with parallel edges.
    If you want a graph with no parallel edges use create_using=Graph()
    but then the resulting degree sequences might not be exact.

    The nodes are assigned the attribute 'bipartite' with the value 0 or 1
    to indicate which bipartite set the node belongs to.

    This function is not imported in the main namespace.
    To use it use nx.bipartite.havel_hakimi_graph
    """
    G = nx.empty_graph(0, create_using, default=nx.MultiGraph)
    if G.is_directed():
        raise nx.NetworkXError("Directed Graph not supported")

    # length of the each sequence
    naseq = len(aseq)
    nbseq = len(bseq)

    suma = sum(aseq)
    sumb = sum(bseq)

    if not suma == sumb:
        raise nx.NetworkXError(
            f"invalid degree sequences, sum(aseq)!=sum(bseq),{suma},{sumb}"
        )

    G = _add_nodes_with_bipartite_label(G, naseq, nbseq)

    if len(aseq) == 0 or max(aseq) == 0:
        return G  # done if no edges

    # build list of degree-repeated vertex numbers
    astubs = [[aseq[v], v] for v in range(naseq)]
    bstubs = [[bseq[v - naseq], v] for v in range(naseq, naseq + nbseq)]
    astubs.sort()
    while astubs:
        (degree, u) = astubs.pop()  # take of largest degree node in the a set
        if degree == 0:
            break  # done, all are zero
        # connect the source to largest degree nodes in the b set
        bstubs.sort()
        for target in bstubs[-degree:]:
            v = target[1]
            G.add_edge(u, v)
            target[0] -= 1  # note this updates bstubs too.
            if target[0] == 0:
                bstubs.remove(target)

    G.name = "bipartite_havel_hakimi_graph"
    return G

