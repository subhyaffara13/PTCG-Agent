
def test_edge_width_sequence(edgelist):
    G = barbell.to_directed()
    pos = nx.random_layout(G)
    widths = (0.5, 2.0, 12.0)
    drawn_edges = nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=widths)
    for fap, expected_width in zip(drawn_edges, itertools.cycle(widths)):
        assert fap.get_linewidth() == expected_width

