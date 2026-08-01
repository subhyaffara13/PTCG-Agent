
def test_display_edge_position(graph_type):
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_node_attributes(G, {n: (n, n) for n in G.nodes()}, "pos")
    ax = plt.figure().add_subplot(111)
    nx.display(G, canvas=ax)
    if G.is_directed():
        end_points = [
            (f.get_path().vertices[0, :], f.get_path().vertices[-2, :])
            for f in ax.get_children()
            if isinstance(f, mpl.patches.FancyArrowPatch)
        ]
    else:
        line_collection = [
            l for l in ax.collections if isinstance(l, mpl.collections.LineCollection)
        ][0]
        end_points = [
            (p.vertices[0, :], p.vertices[-1, :]) for p in line_collection.get_paths()
        ]
    expected = [((0, 0), (1, 1)), ((1, 1), (2, 2))]
    # Use the threshold to account for slight shifts in FancyArrowPatch margins to
    # avoid covering the arrow head with the node.
    threshold = 0.05
    for a, e in zip(end_points, expected):
        act_start, act_end = a
        exp_start, exp_end = e
        assert all(abs(act_start - exp_start) < (threshold, threshold)) and all(
            abs(act_end - exp_end) < (threshold, threshold)
        )
    plt.close()

