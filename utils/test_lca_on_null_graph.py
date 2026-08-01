
def test_lca_on_null_graph():
    G = nx.null_graph(create_using=nx.DiGraph)
    with pytest.raises(
        nx.NetworkXPointlessConcept, match="LCA meaningless on null graphs"
    ):
        nx.lowest_common_ancestor(G, 0, 0)

