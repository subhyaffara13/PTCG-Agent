
def test_random_unlabeled_tree_n_zero():
    """Tests if n = 0 then the NetworkXPointlessConcept exception is raised."""
    with pytest.raises(nx.NetworkXPointlessConcept):
        T = nx.random_unlabeled_tree(0, seed=1234)
    with pytest.raises(nx.NetworkXPointlessConcept):
        T = nx.random_unlabeled_rooted_tree(0, seed=1234)

