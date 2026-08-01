
def test_single_edge_color_directed(edge_color, expected, edgelist):
    """Tests ways of specifying all edges have a single color for edges drawn
    with FancyArrowPatches"""

    G = nx.path_graph(3, create_using=nx.DiGraph)
    drawn_edges = nx.draw_networkx_edges(
        G, pos=nx.random_layout(G), edgelist=edgelist, edge_color=edge_color
    )
    for fap in drawn_edges:
        assert mpl.colors.same_color(fap.get_edgecolor(), expected)

