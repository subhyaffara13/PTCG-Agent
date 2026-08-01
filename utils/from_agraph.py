
def from_agraph(A, create_using=None):
    """Returns a NetworkX Graph or DiGraph from a PyGraphviz graph.

    Parameters
    ----------
    A : PyGraphviz AGraph
      A graph created with PyGraphviz

    create_using : NetworkX graph constructor, optional (default=None)
       Graph type to create. If graph instance, then cleared before populated.
       If `None`, then the appropriate Graph type is inferred from `A`.

    Examples
    --------
    >>> K5 = nx.complete_graph(5)
    >>> A = nx.nx_agraph.to_agraph(K5)
    >>> G = nx.nx_agraph.from_agraph(A)

    Notes
    -----
    The Graph G will have a dictionary G.graph_attr containing
    the default graphviz attributes for graphs, nodes and edges.

    Default node attributes will be in the dictionary G.node_attr
    which is keyed by node.

    Edge attributes will be returned as edge data in G.  With
    edge_attr=False the edge data will be the Graphviz edge weight
    attribute or the value 1 if no edge weight attribute is found.

    """
    if create_using is None:
        if A.is_directed():
            if A.is_strict():
                create_using = nx.DiGraph
            else:
                create_using = nx.MultiDiGraph
        else:
            if A.is_strict():
                create_using = nx.Graph
            else:
                create_using = nx.MultiGraph

    # assign defaults
    N = nx.empty_graph(0, create_using)
    if A.name is not None:
        N.name = A.name

    # add graph attributes
    N.graph.update(A.graph_attr)

    # add nodes, attributes to N.node_attr
    for n in A.nodes():
        str_attr = {str(k): v for k, v in n.attr.items()}
        N.add_node(str(n), **str_attr)

    # add edges, assign edge data as dictionary of attributes
    for e in A.edges():
        u, v = str(e[0]), str(e[1])
        attr = dict(e.attr)
        str_attr = {str(k): v for k, v in attr.items()}
        if not N.is_multigraph():
            if e.name is not None:
                str_attr["key"] = e.name
            N.add_edge(u, v, **str_attr)
        else:
            N.add_edge(u, v, key=e.name, **str_attr)

    # add default attributes for graph, nodes, and edges
    # hang them on N.graph_attr
    graph_default_dict = dict(A.graph_attr)
    if graph_default_dict:
        N.graph["graph"] = graph_default_dict
    node_default_dict = dict(A.node_attr)
    if node_default_dict and node_default_dict != {"label": "\\N"}:
        N.graph["node"] = node_default_dict
    edge_default_dict = dict(A.edge_attr)
    if edge_default_dict:
        N.graph["edge"] = edge_default_dict
    return N

