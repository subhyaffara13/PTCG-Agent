
def test_display_edge_width(param_value, expected, graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, {(0, 1): 5, (1, 2): 10}, "width")
    canvas = plt.figure().add_subplot(111)
    nx.display(G, edge_width=param_value, canvas=canvas)
    if G.is_directed():
        widths = [
            f.get_linewidth()
            for f in canvas.get_children()
            if isinstance(f, mpl.patches.FancyArrowPatch)
        ]
    else:
        widths = list(
            [
                l
                for l in canvas.collections
                if isinstance(l, mpl.collections.LineCollection)
            ][0].get_linewidths()
        )
    assert widths == expected

