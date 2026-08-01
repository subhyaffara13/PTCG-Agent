
def node_link_data(
    G,
    *,
    source="source",
    target="target",
    name="id",
    key="key",
    edges="edges",
    nodes="nodes",
):
    """Returns data in node-link format that is suitable for JSON serialization
    and use in JavaScript documents.

    Parameters
    ----------
    G : NetworkX graph
    source : string
        A string that provides the 'source' attribute name for storing NetworkX-internal graph data.
    target : string
        A string that provides the 'target' attribute name for storing NetworkX-internal graph data.
    name : string
        A string that provides the 'name' attribute name for storing NetworkX-internal graph data.
    key : string
        A string that provides the 'key' attribute name for storing NetworkX-internal graph data.
    edges : string
        A string that provides the 'edges' attribute name for storing NetworkX-internal graph data.
    nodes : string
        A string that provides the 'nodes' attribute name for storing NetworkX-internal graph data.

    Returns
    -------
    data : dict
       A dictionary with node-link formatted data.

    Raises
    ------
    NetworkXError
        If the values of 'source', 'target' and 'key' are not unique.

    Examples
    --------
    >>> from pprint import pprint
    >>> G = nx.Graph([("A", "B")])
    >>> data1 = nx.node_link_data(G)
    >>> pprint(data1)
    {'directed': False,
     'edges': [{'source': 'A', 'target': 'B'}],
     'graph': {},
     'multigraph': False,
     'nodes': [{'id': 'A'}, {'id': 'B'}]}

    To serialize with JSON

    >>> import json
    >>> s1 = json.dumps(data1)
    >>> pprint(s1)
    ('{"directed": false, "multigraph": false, "graph": {}, "nodes": [{"id": "A"}, '
     '{"id": "B"}], "edges": [{"source": "A", "target": "B"}]}')


    A graph can also be serialized by passing `node_link_data` as an encoder function.

    >>> s1 = json.dumps(G, default=nx.node_link_data)
    >>> pprint(s1)
    ('{"directed": false, "multigraph": false, "graph": {}, "nodes": [{"id": "A"}, '
     '{"id": "B"}], "edges": [{"source": "A", "target": "B"}]}')

    The attribute names for storing NetworkX-internal graph data can
    be specified as keyword options.

    >>> H = nx.gn_graph(2)
    >>> data2 = nx.node_link_data(
    ...     H, edges="links", source="from", target="to", nodes="vertices"
    ... )
    >>> pprint(data2)
    {'directed': True,
     'graph': {},
     'links': [{'from': 1, 'to': 0}],
     'multigraph': False,
     'vertices': [{'id': 0}, {'id': 1}]}

    Notes
    -----
    Graph, node, and edge attributes are stored in this format.  Note that
    attribute keys will be converted to strings in order to comply with JSON.

    Attribute 'key' is only used for multigraphs.

    To use `node_link_data` in conjunction with `node_link_graph`,
    the keyword names for the attributes must match.

    See Also
    --------
    node_link_graph, adjacency_data, tree_data
    """
    multigraph = G.is_multigraph()

    # Allow 'key' to be omitted from attrs if the graph is not a multigraph.
    key = None if not multigraph else key
    if len({source, target, key}) < 3:
        raise nx.NetworkXError("Attribute names are not unique.")
    data = {
        "directed": G.is_directed(),
        "multigraph": multigraph,
        "graph": G.graph,
        nodes: [{**G.nodes[n], name: n} for n in G],
    }
    if multigraph:
        data[edges] = [
            {**d, source: u, target: v, key: k}
            for u, v, k, d in G.edges(keys=True, data=True)
        ]
    else:
        data[edges] = [{**d, source: u, target: v} for u, v, d in G.edges(data=True)]
    return data

