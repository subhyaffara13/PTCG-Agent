
def pydot_layout(G, prog="neato", root=None):
    """Create node positions using :mod:`pydot` and Graphviz.

    Parameters
    ----------
    G : Graph
        NetworkX graph to be laid out.
    prog : string  (default: 'neato')
        Name of the GraphViz command to use for layout.
        Options depend on GraphViz version but may include:
        'dot', 'twopi', 'fdp', 'sfdp', 'circo'
    root : Node from G or None (default: None)
        The node of G from which to start some layout algorithms.

    Returns
    -------
    dict
        Dictionary of positions keyed by node.

    Examples
    --------
    >>> G = nx.complete_graph(4)
    >>> pos = nx.nx_pydot.pydot_layout(G)
    >>> pos = nx.nx_pydot.pydot_layout(G, prog="dot")

    Notes
    -----
    If you use complex node objects, they may have the same string
    representation and GraphViz could treat them as the same node.
    The layout may assign both nodes a single location. See Issue #1568
    If this occurs in your case, consider relabeling the nodes just
    for the layout computation using something similar to::

        H = nx.convert_node_labels_to_integers(G, label_attribute="node_label")
        H_layout = nx.nx_pydot.pydot_layout(H, prog="dot")
        G_layout = {H.nodes[n]["node_label"]: p for n, p in H_layout.items()}

    """
    import pydot

    P = to_pydot(G)
    if root is not None:
        P.set("root", str(root))

    # List of low-level bytes comprising a string in the dot language converted
    # from the passed graph with the passed external GraphViz command.
    D_bytes = P.create_dot(prog=prog)

    # Unique string decoded from these bytes with the preferred locale encoding
    D = str(D_bytes, encoding=getpreferredencoding())

    if D == "":  # no data returned
        print(f"Graphviz layout with {prog} failed")
        print()
        print("To debug what happened try:")
        print("P = nx.nx_pydot.to_pydot(G)")
        print('P.write_dot("file.dot")')
        print(f"And then run {prog} on file.dot")
        return

    # List of one or more "pydot.Dot" instances deserialized from this string.
    Q_list = pydot.graph_from_dot_data(D)
    assert len(Q_list) == 1

    # The first and only such instance, as guaranteed by the above assertion.
    Q = Q_list[0]

    node_pos = {}
    for n in G.nodes():
        str_n = str(n)
        node = Q.get_node(pydot.quote_id_if_necessary(str_n))

        if isinstance(node, list):
            node = node[0]
        pos = node.get_pos()[1:-1]  # strip leading and trailing double quotes
        if pos is not None:
            xx, yy = pos.split(",")
            node_pos[n] = (float(xx), float(yy))
    return node_pos

