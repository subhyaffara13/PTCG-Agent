
def test_nonisomorphic_tree_order_1():
    assert nx.number_of_nonisomorphic_trees(1) == 1
    nit_list = list(nx.nonisomorphic_trees(1))
    assert len(nit_list) == 1
    G = nit_list[0]
    assert nx.utils.graphs_equal(G, nx.empty_graph(1))

