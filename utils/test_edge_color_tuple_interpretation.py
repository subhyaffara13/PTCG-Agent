
def test_edge_color_tuple_interpretation():
    """If edge_color is a sequence with the same length as edgelist, then each
    value in edge_color is mapped onto each edge via colormap."""
    G = nx.path_graph(6, create_using=nx.DiGraph)
    pos = {n: (n, n) for n in range(len(G))}

    # num edges != 3 or 4 --> edge_color interpreted as rgb(a)
    for ec in ((0, 0, 1), (0, 0, 1, 1)):
        # More than 4 edges
        drawn_edges = nx.draw_networkx_edges(G, pos, edge_color=ec)
        for fap in drawn_edges:
            assert mpl.colors.same_color(fap.get_edgecolor(), ec)
        # Fewer than 3 edges
        drawn_edges = nx.draw_networkx_edges(
            G, pos, edgelist=[(0, 1), (1, 2)], edge_color=ec
        )
        for fap in drawn_edges:
            assert mpl.colors.same_color(fap.get_edgecolor(), ec)

    # num edges == 3, len(edge_color) == 4: interpreted as rgba
    drawn_edges = nx.draw_networkx_edges(
        G, pos, edgelist=[(0, 1), (1, 2), (2, 3)], edge_color=(0, 0, 1, 1)
    )
    for fap in drawn_edges:
        assert mpl.colors.same_color(fap.get_edgecolor(), "blue")

    # num edges == 4, len(edge_color) == 3: interpreted as rgb
    drawn_edges = nx.draw_networkx_edges(
        G, pos, edgelist=[(0, 1), (1, 2), (2, 3), (3, 4)], edge_color=(0, 0, 1)
    )
    for fap in drawn_edges:
        assert mpl.colors.same_color(fap.get_edgecolor(), "blue")

    # num edges == len(edge_color) == 3: interpreted with cmap, *not* as rgb
    drawn_edges = nx.draw_networkx_edges(
        G, pos, edgelist=[(0, 1), (1, 2), (2, 3)], edge_color=(0, 0, 1)
    )
    assert mpl.colors.same_color(
        drawn_edges[0].get_edgecolor(), drawn_edges[1].get_edgecolor()
    )
    for fap in drawn_edges:
        assert not mpl.colors.same_color(fap.get_edgecolor(), "blue")

    # num edges == len(edge_color) == 4: interpreted with cmap, *not* as rgba
    drawn_edges = nx.draw_networkx_edges(
        G, pos, edgelist=[(0, 1), (1, 2), (2, 3), (3, 4)], edge_color=(0, 0, 1, 1)
    )
    assert mpl.colors.same_color(
        drawn_edges[0].get_edgecolor(), drawn_edges[1].get_edgecolor()
    )
    assert mpl.colors.same_color(
        drawn_edges[2].get_edgecolor(), drawn_edges[3].get_edgecolor()
    )
    for fap in drawn_edges:
        assert not mpl.colors.same_color(fap.get_edgecolor(), "blue")

