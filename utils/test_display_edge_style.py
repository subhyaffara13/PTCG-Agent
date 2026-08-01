
def test_display_edge_style(param_value, expected, graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, {(0, 1): "-", (1, 2): ":"}, "style")
    canvas = plt.figure().add_subplot(111)
    nx.display(G, edge_style=param_value, canvas=canvas)
    if G.is_directed():
        styles = [
            f.get_linestyle()
            for f in canvas.get_children()
            if isinstance(f, mpl.patches.FancyArrowPatch)
        ]
    else:
        # Convert back from tuple description to character form
        linestyles = {(0, None): "-", (0, (1, 1.65)): ":"}
        styles = [
            linestyles[(s[0], tuple(s[1]) if s[1] is not None else None)]
            for s in [
                l
                for l in canvas.collections
                if isinstance(l, mpl.collections.LineCollection)
            ][0].get_linestyles()
        ]
    assert styles == expected
    plt.close()

