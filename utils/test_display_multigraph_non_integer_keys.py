
def test_display_multigraph_non_integer_keys():
    G = nx.MultiGraph()
    G.add_nodes_from(["A", "B", "C", "D"])
    G.add_edges_from(
        [
            ("A", "B", "0"),
            ("A", "B", "1"),
            ("B", "C", "-1"),
            ("B", "C", "1"),
            ("C", "D", "-1"),
            ("C", "D", "0"),
        ]
    )
    nx.set_edge_attributes(
        G, {e: f"arc3,rad={0.2 * int(e[2])}" for e in G.edges(keys=True)}, "curvature"
    )
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas)
    rads = [
        f.get_connectionstyle().rad
        for f in canvas.get_children()
        if isinstance(f, mpl.patches.FancyArrowPatch)
    ]
    assert rads == [0.0, 0.2, -0.2, 0.2, -0.2, 0.0]
    plt.close()

