
def test_set_node_attributes_ignores_extra_nodes(values, name):
    """
    When `values` is a dict or dict-of-dict keyed by nodes, ensure that keys
    that correspond to nodes not in G are ignored.
    """
    G = nx.Graph()
    G.add_node(0)
    nx.set_node_attributes(G, values, name)
    assert G.nodes[0]["color"] == "red"
    assert 1 not in G.nodes

