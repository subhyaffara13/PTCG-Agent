
def test_display_mismatched_edge_position():
    """
    This test ensures that a error is raised for incomplete position data.
    """
    G = nx.path_graph(5)
    # Notice that there is no position for node 3
    nx.set_node_attributes(G, {0: (0, 0), 1: (1, 1), 2: (2, 2), 4: (4, 4)}, "pos")
    # But that's not a problem since we don't want to show node 4, right?
    nx.set_node_attributes(G, {n: n < 4 for n in G.nodes()}, "visible")
    # However, if we try to visualize every edge (including 3 -> 4)...
    # That's a problem since node 4 doesn't have a position
    with pytest.raises(nx.NetworkXError):
        nx.display(G)

