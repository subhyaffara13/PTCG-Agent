
def test_display_arrow_size():
    G = nx.path_graph(4, create_using=nx.DiGraph)
    nx.set_edge_attributes(
        G, {(u, v): (u + v + 2) ** 2 for u, v in G.edges()}, "arrowsize"
    )
    ax = plt.axes()
    nx.display(G, canvas=ax)
    assert [9, 25, 49] == [
        f.get_mutation_scale()
        for f in ax.get_children()
        if isinstance(f, mpl.patches.FancyArrowPatch)
    ]
    plt.close()

