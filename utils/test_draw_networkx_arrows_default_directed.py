
def test_draw_networkx_arrows_default_directed(drawing_func, subplots):
    import matplotlib.collections

    G = nx.path_graph(3, create_using=nx.DiGraph)
    fig, ax = subplots
    drawing_func(G, ax=ax)
    assert not any(
        isinstance(c, mpl.collections.LineCollection) for c in ax.collections
    )
    assert ax.patches

