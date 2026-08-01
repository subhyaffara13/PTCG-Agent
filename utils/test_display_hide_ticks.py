
def test_display_hide_ticks(ticks):
    G = nx.path_graph(3)
    nx.set_node_attributes(G, {n: (n, n) for n in G.nodes()}, "pos")
    ax = plt.axes()
    nx.display(G, hide_ticks=ticks)
    for axis in [ax.xaxis, ax.yaxis]:
        assert bool(axis.get_ticklabels()) != ticks

    plt.close()

