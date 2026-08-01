
def node_attribute_xy(G, attribute, nodes=None):
    """Yields 2-tuples of node attribute values for all edges in `G`.

    This generator yields, for each edge in `G` incident to a node in `nodes`,
    a 2-tuple of form ``(attribute value,  attribute value)`` for the parameter
    specified node-attribute.

    Parameters
    ----------
    G: NetworkX graph

    attribute: key
        The node attribute key.

    nodes: list or iterable (optional)
        Use only edges that are incident to specified nodes.
        The default is all nodes.

    Yields
    ------
    (x, y): 2-tuple
        Generates 2-tuple of (attribute, attribute) values.

    Examples
    --------
    >>> G = nx.DiGraph()
    >>> G.add_node(1, color="red")
    >>> G.add_node(2, color="blue")
    >>> G.add_node(3, color="green")
    >>> G.add_edge(1, 2)
    >>> list(nx.node_attribute_xy(G, "color"))
    [('red', 'blue')]

    Notes
    -----
    For undirected graphs, each edge is produced twice, once for each edge
    representation (u, v) and (v, u), with the exception of self-loop edges
    which only appear once.
    """
    if nodes is None:
        nodes = set(G)
    else:
        nodes = set(nodes)
    Gnodes = G.nodes
    for u, nbrsdict in G.adjacency():
        if u not in nodes:
            continue
        uattr = Gnodes[u].get(attribute, None)
        if G.is_multigraph():
            for v, keys in nbrsdict.items():
                vattr = Gnodes[v].get(attribute, None)
                for _ in keys:
                    yield (uattr, vattr)
        else:
            for v in nbrsdict:
                vattr = Gnodes[v].get(attribute, None)
                yield (uattr, vattr)

