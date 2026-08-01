
def test_hide_ticks(method, hide_ticks, subplots):
    G = nx.path_graph(3)
    pos = {n: (n, n) for n in G.nodes}
    _, ax = subplots
    method(G, pos=pos, ax=ax, hide_ticks=hide_ticks)
    for axis in [ax.xaxis, ax.yaxis]:
        assert bool(axis.get_ticklabels()) != hide_ticks

