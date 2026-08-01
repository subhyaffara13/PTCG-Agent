
def test_tree_isomorphism_raises_on_directed_and_multigraphs(graph_constructor):
    t1 = graph_constructor([(0, 1)])
    t2 = graph_constructor([(1, 2)])
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.isomorphism.tree_isomorphism(t1, t2)

