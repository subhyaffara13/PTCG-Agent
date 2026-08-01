
def test_tree_isomorphism_all_non_isomorphic_pairs(n):
    test_trees = list(nx.nonisomorphic_trees(n))
    assert all(
        nx.isomorphism.tree_isomorphism(test_trees[i], test_trees[j]) == []
        for i in range(len(test_trees) - 1)
        for j in range(i + 1, len(test_trees))
    )

