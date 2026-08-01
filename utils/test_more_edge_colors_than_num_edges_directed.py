
def test_more_edge_colors_than_num_edges_directed():
    """Test that extra edge colors are ignored when there are more specified
    colors than edges."""
    G = nx.path_graph(4, create_using=nx.DiGraph)  # 3 edges
    pos = nx.random_layout(barbell)
    edgecolors = ("r", "g", "b", "c")  # 4 edge colors
    drawn_edges = nx.draw_networkx_edges(G, pos, edge_color=edgecolors)
    for fap, expected in zip(drawn_edges, edgecolors[:-1]):
        assert mpl.colors.same_color(fap.get_edgecolor(), expected)

