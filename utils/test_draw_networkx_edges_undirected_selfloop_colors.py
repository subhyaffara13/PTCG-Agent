
def test_draw_networkx_edges_undirected_selfloop_colors(subplots):
    """When an edgelist is supplied along with a sequence of colors, check that
    the self-loops have the correct colors."""
    fig, ax = subplots
    # Edge list and corresponding colors
    edgelist = [(1, 3), (1, 2), (2, 3), (1, 1), (3, 3), (2, 2)]
    edge_colors = ["pink", "cyan", "black", "red", "blue", "green"]

    G = nx.Graph(edgelist)
    pos = {n: (n, n) for n in G.nodes}
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=edgelist, edge_color=edge_colors)

    # Verify that there are three fancy arrow patches (1 per self loop)
    assert len(ax.patches) == 3

    # These are points that should be contained in the self loops. For example,
    # sl_points[0] will be (1, 1.1), which is inside the "path" of the first
    # self-loop but outside the others
    sl_points = np.array(edgelist[-3:]) + np.array([0, 0.1])

    # Check that the mapping between self-loop locations and their colors is
    # correct
    for fap, clr, slp in zip(ax.patches, edge_colors[-3:], sl_points):
        assert fap.get_path().contains_point(slp)
        assert mpl.colors.same_color(fap.get_edgecolor(), clr)

