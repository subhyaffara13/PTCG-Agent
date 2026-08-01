
def test_input_not_tree():
    tree = nx.Graph([(0, 1), (0, 2)])
    not_tree = nx.cycle_graph(3)

    # tree_isomorphism
    with pytest.raises(nx.NetworkXError, match="t1 is not a tree"):
        nx.isomorphism.tree_isomorphism(not_tree, tree)
    with pytest.raises(nx.NetworkXError, match="t2 is not a tree"):
        nx.isomorphism.tree_isomorphism(tree, not_tree)

    # rooted_tree_isomorphism
    with pytest.raises(nx.NetworkXError, match="t1 is not a tree"):
        nx.isomorphism.rooted_tree_isomorphism(not_tree, 0, tree, 0)
    with pytest.raises(nx.NetworkXError, match="t2 is not a tree"):
        nx.isomorphism.rooted_tree_isomorphism(tree, 0, not_tree, 0)

