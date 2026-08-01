
def test_display_edge_colormaps(graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, {(0, 1): 0, (1, 2): 1}, "weight")
    cmap = mpl.colormaps["plasma"]
    nx.apply_matplotlib_colors(G, "weight", "color", cmap, nodes=False)
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas)
    mapper = mpl.cm.ScalarMappable(cmap=cmap)
    mapper.set_clim(0, 1)
    expected = [mapper.to_rgba(0), mapper.to_rgba(1)]
    if G.is_directed():
        colors = [
            f.get_facecolor()
            for f in canvas.get_children()
            if isinstance(f, mpl.patches.FancyArrowPatch)
        ]
    else:
        colors = [
            l
            for l in canvas.collections
            if isinstance(l, mpl.collections.LineCollection)
        ][0].get_colors()
    assert mpl.colors.same_color(expected[0], G.edges[0, 1]["color"])
    assert mpl.colors.same_color(expected[1], G.edges[1, 2]["color"])
    assert mpl.colors.same_color(expected, colors)
    plt.close()

