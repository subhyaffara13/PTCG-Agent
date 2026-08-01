
def test_random_spanning_tree_empty_graph():
    G = nx.Graph()
    rst = nx.tree.random_spanning_tree(G)
    assert len(rst.nodes) == 0
    assert len(rst.edges) == 0

