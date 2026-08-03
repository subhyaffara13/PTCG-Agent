import copy

def contracted_nodes(
    G, u, v, self_loops=True, copy=True, *, store_contraction_as="contraction"
):
    """Returns the graph that results from contracting `u` and `v`.

    Node contraction identifies the two nodes as a single node incident to any
    edge that was incident to the original two nodes.
    Information about the contracted nodes and any modified edges are stored on
    the output graph in a ``"contraction"`` attribute - see Examples for details.

    Parameters
    ----------
    G : NetworkX graph
        The graph whose nodes will be contracted.

    u, v : nodes
        Must be nodes in `G`.

    self_loops : Boolean
        If this is True, any edges joining `u` and `v` in `G` become
        self-loops on the new node in the returned graph.

    copy : Boolean
        If this is True (the default), make a copy of
        `G` and return that instead of directly changing `G`.

    store_contraction_as : str or None, default="contraction"
        Name of the node/edge attribute where information about the contraction
        should be stored. By default information about the contracted node and
        any contracted edges is stored in a ``"contraction"`` attribute on the
        resulting node and edge. If `None`, information about the contracted
        nodes/edges and their data are not stored.

    Returns
    -------
    Networkx graph
        If `copy` is True,
        A new graph object of the same type as `G` (leaving `G` unmodified)
        with `u` and `v` identified in a single node. The right node `v`
        will be merged into the node `u`, so only `u` will appear in the
        returned graph.
        If `copy` is False,
        Modifies `G` with `u` and `v` identified in a single node.
        The right node `v` will be merged into the node `u`, so
        only `u` will appear in the returned graph.

    Notes
    -----
    For multigraphs, the edge keys for the realigned edges may
    not be the same as the edge keys for the old edges. This is
    natural because edge keys are unique only within each pair of nodes.

    This function is also available as `identified_nodes`.

    Examples
    --------
    Contracting two nonadjacent nodes of the cycle graph on four nodes `C_4`
    yields the path graph (ignoring parallel edges):

    >>> G = nx.cycle_graph(4)
    >>> M = nx.contracted_nodes(G, 1, 3)
    >>> P3 = nx.path_graph(3)
    >>> nx.is_isomorphic(M, P3)
    True

    Information about the contracted nodes is stored on the resulting graph in
    a ``"contraction"`` attribute. For instance, the contracted node is stored
    as an attribute on ``u``:

    >>> H = nx.contracted_nodes(P3, 0, 2)
    >>> H.nodes(data=True)
    NodeDataView({0: {'contraction': {2: {}}}, 1: {}})

    Any node attributes on the contracted node are also preserved:

    >>> nx.set_node_attributes(P3, dict(enumerate("rgb")), name="color")
    >>> P3.nodes(data=True)
    NodeDataView({0: {'color': 'r'}, 1: {'color': 'g'}, 2: {'color': 'b'}})
    >>> H = nx.contracted_nodes(P3, 0, 2)
    >>> H.nodes[0]
    {'color': 'r', 'contraction': {2: {'color': 'b'}}}

    Edges are handled similarly: when ``u`` and ``v`` are adjacent to a third node
    ``w``, the edge ``(v, w)`` will be contracted into the edge ``(u, w)`` with
    its attributes stored into a ``"contraction"`` attribute on edge ``(u, w)``:

    >>> nx.set_edge_attributes(P3, {(0, 1): 10, (1, 2): 100}, name="weight")
    >>> P3.edges(data=True)
    EdgeDataView([(0, 1, {'weight': 10}), (1, 2, {'weight': 100})])
    >>> H = nx.contracted_nodes(P3, 0, 2)
    >>> H.edges(data=True)
    EdgeDataView([(0, 1, {'weight': 10, 'contraction': {(2, 1): {'weight': 100}}})])

    Attributes from contracted nodes/edges can be combined with those of the
    nodes/edges onto which they were contracted:

    >>> # Concatenate colors of contracted nodes
    >>> for u, cdict in H.nodes(data="contraction"):
    ...     if cdict is not None:
    ...         H.nodes[u]["color"] += "".join(n["color"] for n in cdict.values())
    ...         del H.nodes[u]["contraction"]  # Remove contraction attr (optional)
    >>> H.nodes(data=True)
    NodeDataView({0: {'color': 'rb'}, 1: {'color': 'g'}})
    >>> # Sum contracted edge weights
    >>> for u, v, cdict in H.edges(data="contraction"):
    ...     if cdict is not None:
    ...         H[u][v]["weight"] += sum(n["weight"] for n in cdict.values())
    ...         del H.edges[(u, v)]["contraction"]  # Remove contraction attr (optional)
    >>> H.edges(data=True)
    EdgeDataView([(0, 1, {'weight': 110})])

    If `G` is a multigraph, then a new edge is added instead. Any edge attributes
    are still preserved:

    >>> MG = nx.MultiGraph(P3)
    >>> MH = nx.contracted_nodes(MG, 0, 2)
    >>> MH.edges(keys=True, data=True)
    MultiEdgeDataView([(0, 1, 0, {'weight': 10}), (0, 1, 1, {'weight': 100})])

    If ``selfloops=True`` (the default), any edges adjoining `u` and `v` become
    self-loops on ``u`` in the resulting graph:

    >>> G = nx.Graph([(1, 2)])
    >>> H = nx.contracted_nodes(G, 1, 2)
    >>> H.nodes, H.edges
    (NodeView((1,)), EdgeView([(1, 1)]))
    >>> H = nx.contracted_nodes(G, 1, 2, self_loops=False)
    >>> H.nodes, H.edges
    (NodeView((1,)), EdgeView([]))

    Note however that any self loops in the original graph `G` are preserved:

    >>> G = nx.Graph([(1, 2), (2, 2)])
    >>> H = nx.contracted_nodes(G, 1, 2, self_loops=False)
    >>> H.nodes, H.edges
    (NodeView((1,)), EdgeView([(1, 1)]))

    The same reasoning applies to MultiGraphs:

    >>> MG = nx.MultiGraph([(1, 2), (2, 2)])
    >>> # Edge (1, 1, 0) in MH corresponds to edge (2, 2) in MG
    >>> MH = nx.contracted_nodes(MG, 1, 2, self_loops=False)
    >>> MH.edges(keys=True)
    MultiEdgeView([(1, 1, 0)])
    >>> # MH has two (1, 1) edges - one from edge (2, 2) in MG, and one
    >>> # resulting from the contraction of 2->1
    >>> MH = nx.contracted_nodes(MG, 1, 2, self_loops=True)
    >>> MH.edges(keys=True)
    MultiEdgeView([(1, 1, 0), (1, 1, 1)])


    In a ``MultiDiGraph`` with a self loop, the in and out edges will
    be treated separately as edges, so while contracting a node which
    has a self loop the contraction will add multiple edges:

    >>> G = nx.MultiDiGraph([(1, 2), (2, 2)])
    >>> H = nx.contracted_nodes(G, 1, 2)
    >>> list(H.edges())  # edge 1->2, 2->2, 2<-2 from the original Graph G
    [(1, 1), (1, 1), (1, 1)]
    >>> H = nx.contracted_nodes(G, 1, 2, self_loops=False)
    >>> list(H.edges())  # edge 2->2, 2<-2 from the original Graph G
    [(1, 1), (1, 1)]

    See Also
    --------
    contracted_edge
    quotient_graph

    """
    # Copying has significant overhead and can be disabled if needed
    H = G.copy() if copy else G

    # edge code uses G.edges(v) instead of G.adj[v] to handle multiedges
    if H.is_directed():
        edges_to_remap = chain(G.in_edges(v, data=True), G.out_edges(v, data=True))
    else:
        edges_to_remap = G.edges(v, data=True)

    # If the H=G, the generators change as H changes
    # This makes the edges_to_remap independent of H
    if not copy:
        edges_to_remap = list(edges_to_remap)

    v_data = H.nodes[v]
    H.remove_node(v)

    # A bit of input munging to extract whether contraction info should be
    # stored, and if so bind to a shorter name
    if _store_contraction := (store_contraction_as is not None):
        contraction = store_contraction_as

    for prev_w, prev_x, d in edges_to_remap:
        w = prev_w if prev_w != v else u
        x = prev_x if prev_x != v else u

        if ({prev_w, prev_x} == {u, v}) and not self_loops:
            continue

        if not H.has_edge(w, x) or G.is_multigraph():
            H.add_edge(w, x, **d)
            continue

        # Store information about the contracted edge iff `store_contraction` is not None
        if _store_contraction:
            if contraction in H.edges[(w, x)]:
                H.edges[(w, x)][contraction][(prev_w, prev_x)] = d
            else:
                H.edges[(w, x)][contraction] = {(prev_w, prev_x): d}

    # Store information about the contracted node iff `store_contraction`
    if _store_contraction:
        if contraction in H.nodes[u]:
            H.nodes[u][contraction][v] = v_data
        else:
            H.nodes[u][contraction] = {v: v_data}

    return H

