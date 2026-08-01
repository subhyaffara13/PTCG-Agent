
def test_lca_on_cycle_graph():
    G = nx.cycle_graph(6, create_using=nx.DiGraph)
    with pytest.raises(
        nx.NetworkXError, match="LCA only defined on directed acyclic graphs"
    ):
        nx.lowest_common_ancestor(G, 0, 3)

