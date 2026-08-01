
def test_multipartite_layout_layer_order():
    """Return the layers in sorted order if the layers of the multipartite
    graph are sortable. See gh-5691"""
    G = nx.Graph()
    node_group = dict(zip(("a", "b", "c", "d", "e"), (2, 3, 1, 2, 4)))
    for node, layer in node_group.items():
        G.add_node(node, subset=layer)

    # Horizontal alignment, therefore y-coord determines layers
    pos = nx.multipartite_layout(G, align="horizontal")

    layers = nx.utils.groups(node_group)
    pos_from_layers = nx.multipartite_layout(G, align="horizontal", subset_key=layers)
    for (n1, p1), (n2, p2) in zip(pos.items(), pos_from_layers.items()):
        assert n1 == n2 and (p1 == p2).all()

    # Nodes "a" and "d" are in the same layer
    assert pos["a"][-1] == pos["d"][-1]
    # positions should be sorted according to layer
    assert pos["c"][-1] < pos["a"][-1] < pos["b"][-1] < pos["e"][-1]

    # Make sure that multipartite_layout still works when layers are not sortable
    G.nodes["a"]["subset"] = "layer_0"  # Can't sort mixed strs/ints
    pos_nosort = nx.multipartite_layout(G)  # smoke test: this should not raise
    assert pos_nosort.keys() == pos.keys()

