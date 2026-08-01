
def test_draw_edges_toggling_with_arrows_kwarg():
    """
    The `arrows` keyword argument is used as a 3-way switch to select which
    type of object to use for drawing edges:
      - ``arrows=None`` -> default (FancyArrowPatches for directed, else LineCollection)
      - ``arrows=True`` -> FancyArrowPatches
      - ``arrows=False`` -> LineCollection
    """
    import matplotlib.collections
    import matplotlib.patches

    UG = nx.path_graph(3)
    DG = nx.path_graph(3, create_using=nx.DiGraph)
    pos = {n: (n, n) for n in UG}

    # Use FancyArrowPatches when arrows=True, regardless of graph type
    for G in (UG, DG):
        edges = nx.draw_networkx_edges(G, pos, arrows=True)
        assert len(edges) == len(G.edges)
        assert isinstance(edges[0], mpl.patches.FancyArrowPatch)

    # Use LineCollection when arrows=False, regardless of graph type
    for G in (UG, DG):
        edges = nx.draw_networkx_edges(G, pos, arrows=False)
        assert isinstance(edges, mpl.collections.LineCollection)

    # Default behavior when arrows=None: FAPs for directed, LC's for undirected
    edges = nx.draw_networkx_edges(UG, pos)
    assert isinstance(edges, mpl.collections.LineCollection)
    edges = nx.draw_networkx_edges(DG, pos)
    assert len(edges) == len(G.edges)
    assert isinstance(edges[0], mpl.patches.FancyArrowPatch)

