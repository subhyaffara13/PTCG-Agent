
def graphviz_layout(G, prog="neato", root=None, args=""):
    """Create node positions for G using Graphviz.

    Parameters
    ----------
    G : NetworkX graph
      A graph created with NetworkX
    prog : string
      Name of Graphviz layout program
    root : string, optional
      Root node for twopi layout
    args : string, optional
      Extra arguments to Graphviz layout program

    Returns
    -------
    Dictionary of x, y, positions keyed by node.

    Examples
    --------
    >>> G = nx.petersen_graph()
    >>> pos = nx.nx_agraph.graphviz_layout(G)
    >>> pos = nx.nx_agraph.graphviz_layout(G, prog="dot")

    Notes
    -----
    This is a wrapper for pygraphviz_layout.

    Note that some graphviz layouts are not guaranteed to be deterministic,
    see https://gitlab.com/graphviz/graphviz/-/issues/1767 for more info.
    """
    return pygraphviz_layout(G, prog=prog, root=root, args=args)


def graphviz_layout(G, prog="neato", root=None):
    """Create node positions using Pydot and Graphviz.

    Returns a dictionary of positions keyed by node.

    Parameters
    ----------
    G : NetworkX Graph
        The graph for which the layout is computed.
    prog : string (default: 'neato')
        The name of the GraphViz program to use for layout.
        Options depend on GraphViz version but may include:
        'dot', 'twopi', 'fdp', 'sfdp', 'circo'
    root : Node from G or None (default: None)
        The node of G from which to start some layout algorithms.

    Returns
    -------
      Dictionary of (x, y) positions keyed by node.

    Examples
    --------
    >>> G = nx.complete_graph(4)
    >>> pos = nx.nx_pydot.graphviz_layout(G)
    >>> pos = nx.nx_pydot.graphviz_layout(G, prog="dot")

    Notes
    -----
    This is a wrapper for pydot_layout.
    """
    return pydot_layout(G=G, prog=prog, root=root)

