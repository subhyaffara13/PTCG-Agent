
def test_draw_networkx_nodes_node_shape_list_with_scalar_color(subplots):
    """Ensure draw_networkx_nodes works when node_shape is a Python list.

    This covers the case where node_shape is a sequence (list) and node_color
    is a single scalar color, which should be supported.
    """
    fig, ax = subplots

    G = nx.empty_graph(5)
    pos = {i: (i, i) for i in G}

    shapes = ["o", "^", "o", "^", "o"]

    nodes = nx.draw_networkx_nodes(
        G,
        pos,
        node_color="red",  # scalar color (supported)
        node_shape=shapes,  # list of shapes – this used to be buggy
        ax=ax,
    )
    # Should get a PathCollection with an element in it (same as with numpy arrays)
    assert len(nodes.get_offsets()) > 0

