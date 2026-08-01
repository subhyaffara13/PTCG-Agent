
def remove_node_attributes(G, *attr_names, nbunch=None):
    """Remove node attributes from all nodes in the graph.

    Parameters
    ----------
    G : NetworkX Graph

    *attr_names : List of Strings
        The attribute names to remove from the graph.

    nbunch : List of Nodes
        Remove the node attributes only from the nodes in this list.

    Examples
    --------
    >>> G = nx.Graph()
    >>> G.add_nodes_from([1, 2, 3], color="blue")
    >>> nx.get_node_attributes(G, "color")
    {1: 'blue', 2: 'blue', 3: 'blue'}
    >>> nx.remove_node_attributes(G, "color")
    >>> nx.get_node_attributes(G, "color")
    {}
    """

    if nbunch is None:
        nbunch = G.nodes()

    for attr in attr_names:
        for n, d in G.nodes(data=True):
            if n in nbunch:
                try:
                    del d[attr]
                except KeyError:
                    pass

