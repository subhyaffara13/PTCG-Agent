
def test_return_types():
    from matplotlib.collections import LineCollection, PathCollection
    from matplotlib.patches import FancyArrowPatch

    G = nx.frucht_graph(create_using=nx.Graph)
    dG = nx.frucht_graph(create_using=nx.DiGraph)
    pos = nx.spring_layout(G, seed=42)
    dpos = nx.spring_layout(dG, seed=42)
    # nodes
    nodes = nx.draw_networkx_nodes(G, pos)
    assert isinstance(nodes, PathCollection)
    # edges
    edges = nx.draw_networkx_edges(dG, dpos, arrows=True)
    assert isinstance(edges, list)
    if len(edges) > 0:
        assert isinstance(edges[0], FancyArrowPatch)
    edges = nx.draw_networkx_edges(dG, dpos, arrows=False)
    assert isinstance(edges, LineCollection)
    edges = nx.draw_networkx_edges(G, dpos, arrows=None)
    assert isinstance(edges, LineCollection)
    edges = nx.draw_networkx_edges(dG, pos, arrows=None)
    assert isinstance(edges, list)
    if len(edges) > 0:
        assert isinstance(edges[0], FancyArrowPatch)

