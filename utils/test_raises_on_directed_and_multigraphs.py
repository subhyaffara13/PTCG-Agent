
def test_raises_on_directed_and_multigraphs(f, graph_constructor):
    G = graph_constructor([(0, 1), (1, 2)])
    with pytest.raises(nx.NetworkXNotImplemented):
        f(G)


def test_raises_on_directed_and_multigraphs(graph_constructor):
    G = graph_constructor([(0, 1), (1, 2)])
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.community.asyn_fluidc(G, 1)


def test_raises_on_directed_and_multigraphs(f, graph_constructor):
    G = graph_constructor([(0, 1), (1, 2)])
    with pytest.raises(nx.NetworkXNotImplemented):
        f(G)

