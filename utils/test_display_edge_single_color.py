
def test_display_edge_single_color(edge_color, expected, graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, "#0000FF", "color")
    canvas = plt.figure().add_subplot(111)
    nx.display(G, edge_color=edge_color, canvas=canvas)
    if G.is_directed():
        colors = [
            f.get_fc()
            for f in canvas.get_children()
            if isinstance(f, mpl.patches.FancyArrowPatch)
        ]
    else:
        colors = [
            l
            for l in canvas.collections
            if isinstance(l, mpl.collections.LineCollection)
        ][0].get_colors()
    assert all(mpl.colors.same_color(c, expected) for c in colors)
    plt.close()

