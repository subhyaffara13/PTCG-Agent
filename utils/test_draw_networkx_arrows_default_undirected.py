
def test_draw_networkx_arrows_default_undirected(drawing_func, subplots):
    import matplotlib.collections

    G = nx.path_graph(3)
    fig, ax = subplots
    drawing_func(G, ax=ax)
    assert any(isinstance(c, mpl.collections.LineCollection) for c in ax.collections)
    assert not ax.patches

