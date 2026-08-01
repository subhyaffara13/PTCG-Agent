
def test_constraint_isolated_node_with_selfloop_weighted_using_nodes_kwarg(graph):
    G = graph()
    G.add_weighted_edges_from([(0, 0, 10)])
    assert nx.constraint(G, nodes=[0])[0] == 4

