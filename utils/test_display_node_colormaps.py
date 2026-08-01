
def test_display_node_colormaps(graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_node_attributes(G, {0: 0, 1: 0.5, 2: 1}, "weight")
    cmap = mpl.colormaps["plasma"]
    nx.apply_matplotlib_colors(G, "weight", "color", cmap)
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas)
    mapper = mpl.cm.ScalarMappable(cmap=cmap)
    mapper.set_clim(0, 1)
    expected = [mapper.to_rgba(0), mapper.to_rgba(0.5), mapper.to_rgba(1)]
    colors = [
        s for s in canvas.collections if isinstance(s, mpl.collections.PathCollection)
    ][0].get_edgecolors()
    assert mpl.colors.same_color(expected[0], G.nodes[0]["color"])
    assert mpl.colors.same_color(expected[1], G.nodes[1]["color"])
    assert mpl.colors.same_color(expected[2], G.nodes[2]["color"])
    assert mpl.colors.same_color(expected, colors)
    plt.close()

