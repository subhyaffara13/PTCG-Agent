
def local_node_connectivity(G, source, target, cutoff=None):
    """Compute node connectivity between source and target.

    Pairwise or local node connectivity between two distinct and nonadjacent
    nodes is the minimum number of nodes that must be removed (minimum
    separating cutset) to disconnect them. By Menger's theorem, this is equal
    to the number of node independent paths (paths that share no nodes other
    than source and target). Which is what we compute in this function.

    This algorithm is a fast approximation that gives an strict lower
    bound on the actual number of node independent paths between two nodes [1]_.
    It works for both directed and undirected graphs.

    Parameters
    ----------

    G : NetworkX graph

    source : node
        Starting node for node connectivity

    target : node
        Ending node for node connectivity

    cutoff : integer
        Maximum node connectivity to consider. If None, the minimum degree
        of source or target is used as a cutoff. Default value None.

    Returns
    -------
    k: integer
       pairwise node connectivity

    Examples
    --------
    >>> # Platonic octahedral graph has node connectivity 4
    >>> # for each non adjacent node pair
    >>> from networkx.algorithms import approximation as approx
    >>> G = nx.octahedral_graph()
    >>> approx.local_node_connectivity(G, 0, 5)
    4

    Notes
    -----
    This algorithm [1]_ finds node independents paths between two nodes by
    computing their shortest path using BFS, marking the nodes of the path
    found as 'used' and then searching other shortest paths excluding the
    nodes marked as used until no more paths exist. It is not exact because
    a shortest path could use nodes that, if the path were longer, may belong
    to two different node independent paths. Thus it only guarantees an
    strict lower bound on node connectivity.

    Note that the authors propose a further refinement, losing accuracy and
    gaining speed, which is not implemented yet.

    See also
    --------
    all_pairs_node_connectivity
    node_connectivity

    References
    ----------
    .. [1] White, Douglas R., and Mark Newman. 2001 A Fast Algorithm for
        Node-Independent Paths. Santa Fe Institute Working Paper #01-07-035
        http://eclectic.ss.uci.edu/~drwhite/working.pdf

    """
    if target == source:
        raise nx.NetworkXError("source and target have to be different nodes.")

    # Maximum possible node independent paths
    if G.is_directed():
        possible = min(G.out_degree(source), G.in_degree(target))
    else:
        possible = min(G.degree(source), G.degree(target))

    K = 0
    if not possible:
        return K

    if cutoff is None:
        cutoff = float("inf")

    exclude = set()
    for i in range(min(possible, cutoff)):
        try:
            path = _bidirectional_shortest_path(G, source, target, exclude)
            exclude.update(set(path))
            K += 1
        except nx.NetworkXNoPath:
            break

    return K


def local_node_connectivity(
    G, s, t, flow_func=None, auxiliary=None, residual=None, cutoff=None
):
    r"""Computes local node connectivity for nodes s and t.

    Local node connectivity for two non adjacent nodes s and t is the
    minimum number of nodes that must be removed (along with their incident
    edges) to disconnect them.

    This is a flow based implementation of node connectivity. We compute the
    maximum flow on an auxiliary digraph build from the original input
    graph (see below for details).

    Parameters
    ----------
    G : NetworkX graph
        Undirected graph

    s : node
        Source node

    t : node
        Target node

    flow_func : function
        A function for computing the maximum flow among a pair of nodes.
        The function has to accept at least three parameters: a Digraph,
        a source node, and a target node. And return a residual network
        that follows NetworkX conventions (see :meth:`maximum_flow` for
        details). If flow_func is None, the default maximum flow function
        (:meth:`edmonds_karp`) is used. See below for details. The choice
        of the default function may change from version to version and
        should not be relied on. Default value: None.

    auxiliary : NetworkX DiGraph
        Auxiliary digraph to compute flow based node connectivity. It has
        to have a graph attribute called mapping with a dictionary mapping
        node names in G and in the auxiliary digraph. If provided
        it will be reused instead of recreated. Default value: None.

    residual : NetworkX DiGraph
        Residual network to compute maximum flow. If provided it will be
        reused instead of recreated. Default value: None.

    cutoff : integer, float, or None (default: None)
        If specified, the maximum flow algorithm will terminate when the
        flow value reaches or exceeds the cutoff. This only works for flows
        that support the cutoff parameter (most do) and is ignored otherwise.

    Returns
    -------
    K : integer
        local node connectivity for nodes s and t

    Examples
    --------
    This function is not imported in the base NetworkX namespace, so you
    have to explicitly import it from the connectivity package:

    >>> from networkx.algorithms.connectivity import local_node_connectivity

    We use in this example the platonic icosahedral graph, which has node
    connectivity 5.

    >>> G = nx.icosahedral_graph()
    >>> local_node_connectivity(G, 0, 6)
    5

    If you need to compute local connectivity on several pairs of
    nodes in the same graph, it is recommended that you reuse the
    data structures that NetworkX uses in the computation: the
    auxiliary digraph for node connectivity, and the residual
    network for the underlying maximum flow computation.

    Example of how to compute local node connectivity among
    all pairs of nodes of the platonic icosahedral graph reusing
    the data structures.

    >>> import itertools
    >>> # You also have to explicitly import the function for
    >>> # building the auxiliary digraph from the connectivity package
    >>> from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
    >>> H = build_auxiliary_node_connectivity(G)
    >>> # And the function for building the residual network from the
    >>> # flow package
    >>> from networkx.algorithms.flow import build_residual_network
    >>> # Note that the auxiliary digraph has an edge attribute named capacity
    >>> R = build_residual_network(H, "capacity")
    >>> result = dict.fromkeys(G, dict())
    >>> # Reuse the auxiliary digraph and the residual network by passing them
    >>> # as parameters
    >>> for u, v in itertools.combinations(G, 2):
    ...     k = local_node_connectivity(G, u, v, auxiliary=H, residual=R)
    ...     result[u][v] = k
    >>> all(result[u][v] == 5 for u, v in itertools.combinations(G, 2))
    True

    You can also use alternative flow algorithms for computing node
    connectivity. For instance, in dense networks the algorithm
    :meth:`shortest_augmenting_path` will usually perform better than
    the default :meth:`edmonds_karp` which is faster for sparse
    networks with highly skewed degree distributions. Alternative flow
    functions have to be explicitly imported from the flow package.

    >>> from networkx.algorithms.flow import shortest_augmenting_path
    >>> local_node_connectivity(G, 0, 6, flow_func=shortest_augmenting_path)
    5

    Notes
    -----
    This is a flow based implementation of node connectivity. We compute the
    maximum flow using, by default, the :meth:`edmonds_karp` algorithm (see:
    :meth:`maximum_flow`) on an auxiliary digraph build from the original
    input graph:

    For an undirected graph G having `n` nodes and `m` edges we derive a
    directed graph H with `2n` nodes and `2m+n` arcs by replacing each
    original node `v` with two nodes `v_A`, `v_B` linked by an (internal)
    arc in H. Then for each edge (`u`, `v`) in G we add two arcs
    (`u_B`, `v_A`) and (`v_B`, `u_A`) in H. Finally we set the attribute
    capacity = 1 for each arc in H [1]_ .

    For a directed graph G having `n` nodes and `m` arcs we derive a
    directed graph H with `2n` nodes and `m+n` arcs by replacing each
    original node `v` with two nodes `v_A`, `v_B` linked by an (internal)
    arc (`v_A`, `v_B`) in H. Then for each arc (`u`, `v`) in G we add one arc
    (`u_B`, `v_A`) in H. Finally we set the attribute capacity = 1 for
    each arc in H.

    This is equal to the local node connectivity because the value of
    a maximum s-t-flow is equal to the capacity of a minimum s-t-cut.

    See also
    --------
    :meth:`local_edge_connectivity`
    :meth:`node_connectivity`
    :meth:`minimum_node_cut`
    :meth:`maximum_flow`
    :meth:`edmonds_karp`
    :meth:`preflow_push`
    :meth:`shortest_augmenting_path`

    References
    ----------
    .. [1] Kammer, Frank and Hanjo Taubig. Graph Connectivity. in Brandes and
        Erlebach, 'Network Analysis: Methodological Foundations', Lecture
        Notes in Computer Science, Volume 3418, Springer-Verlag, 2005.
        http://www.informatik.uni-augsburg.de/thi/personen/kammer/Graph_Connectivity.pdf

    """
    if flow_func is None:
        flow_func = default_flow_func

    if auxiliary is None:
        H = build_auxiliary_node_connectivity(G)
    else:
        H = auxiliary

    mapping = H.graph.get("mapping", None)
    if mapping is None:
        raise nx.NetworkXError("Invalid auxiliary digraph.")

    kwargs = {"flow_func": flow_func, "residual": residual}

    if flow_func is not preflow_push:
        kwargs["cutoff"] = cutoff

    if flow_func is shortest_augmenting_path:
        kwargs["two_phase"] = True

    return nx.maximum_flow_value(H, f"{mapping[s]}B", f"{mapping[t]}A", **kwargs)

