
def alternating_havel_hakimi_graph(aseq, bseq, create_using=None):
    """Returns a bipartite graph from two given degree sequences using
    an alternating Havel-Hakimi style construction.

    The graph is composed of two partitions. Set A has nodes 0 to
    (len(aseq) - 1) and set B has nodes len(aseq) to (len(bseq) - 1).
    Nodes from the set A are connected to nodes in the set B by
    connecting the highest degree nodes in set A to alternatively the
    highest and the lowest degree nodes in set B until all stubs are
    connected.

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
    To use it use nx.bipartite.alternating_havel_hakimi_graph
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
    while astubs:
        astubs.sort()
        (degree, u) = astubs.pop()  # take of largest degree node in the a set
        if degree == 0:
            break  # done, all are zero
        bstubs.sort()
        small = bstubs[0 : degree // 2]  # add these low degree targets
        large = bstubs[(-degree + degree // 2) :]  # now high degree targets
        stubs = [x for z in zip(large, small) for x in z]  # combine, sorry
        if len(stubs) < len(small) + len(large):  # check for zip truncation
            stubs.append(large.pop())
        for target in stubs:
            v = target[1]
            G.add_edge(u, v)
            target[0] -= 1  # note this updates bstubs too.
            if target[0] == 0:
                bstubs.remove(target)

    G.name = "bipartite_alternating_havel_hakimi_graph"
    return G

