
def to_agraph(N):
    """Returns a pygraphviz graph from a NetworkX graph N.

    Parameters
    ----------
    N : NetworkX graph
      A graph created with NetworkX

    Examples
    --------
    >>> K5 = nx.complete_graph(5)
    >>> A = nx.nx_agraph.to_agraph(K5)

    Notes
    -----
    If N has an dict N.graph_attr an attempt will be made first
    to copy properties attached to the graph (see from_agraph)
    and then updated with the calling arguments if any.

    """
    try:
        import pygraphviz
    except ImportError as err:
        raise ImportError("requires pygraphviz http://pygraphviz.github.io/") from err
    directed = N.is_directed()
    strict = nx.number_of_selfloops(N) == 0 and not N.is_multigraph()

    A = pygraphviz.AGraph(name=N.name, strict=strict, directed=directed)

    # default graph attributes
    A.graph_attr.update(N.graph.get("graph", {}))
    A.node_attr.update(N.graph.get("node", {}))
    A.edge_attr.update(N.graph.get("edge", {}))

    A.graph_attr.update(
        (k, v) for k, v in N.graph.items() if k not in ("graph", "node", "edge")
    )

    # add nodes
    for n, nodedata in N.nodes(data=True):
        A.add_node(n)
        # Add node data
        a = A.get_node(n)
        for key, val in nodedata.items():
            if key == "pos":
                a.attr["pos"] = f"{val[0]},{val[1]}!"
            else:
                a.attr[key] = str(val)

    # loop over edges
    if N.is_multigraph():
        for u, v, key, edgedata in N.edges(data=True, keys=True):
            str_edgedata = {k: str(v) for k, v in edgedata.items() if k != "key"}
            A.add_edge(u, v, key=str(key))
            # Add edge data
            a = A.get_edge(u, v)
            a.attr.update(str_edgedata)

    else:
        for u, v, edgedata in N.edges(data=True):
            str_edgedata = {k: str(v) for k, v in edgedata.items()}
            A.add_edge(u, v)
            # Add edge data
            a = A.get_edge(u, v)
            a.attr.update(str_edgedata)

    return A

