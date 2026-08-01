
def test_display_line_collection():
    G = nx.karate_club_graph()
    nx.set_edge_attributes(
        G, {(u, v): "-|>" if (u + v) % 2 else "-" for u, v in G.edges()}, "arrowstyle"
    )
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas, edge_arrowsize=10)
    # There should only be one line collection in any given visualization
    lc = [
        l
        for l in canvas.get_children()
        if isinstance(l, mpl.collections.LineCollection)
    ][0]
    assert len(lc.get_paths()) == sum([1 for u, v in G.edges() if (u + v) % 2])
    plt.close()

