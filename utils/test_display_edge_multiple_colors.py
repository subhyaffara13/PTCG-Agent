
def test_display_edge_multiple_colors(graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, {(0, 1): "#FF0000", (1, 2): (0, 0, 1)}, "color")
    ax = plt.figure().add_subplot(111)
    nx.display(G, canvas=ax)
    expected = ["red", "blue"]
    if G.is_directed():
        colors = [
            f.get_fc()
            for f in ax.get_children()
            if isinstance(f, mpl.patches.FancyArrowPatch)
        ]
    else:
        colors = [
            l for l in ax.collections if isinstance(l, mpl.collections.LineCollection)
        ][0].get_colors()
    assert mpl.colors.same_color(colors, expected)
    plt.close()

