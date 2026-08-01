
def test_nonisomorphic_tree_negative_order():
    with pytest.raises(ValueError, match="order must be non-negative"):
        nx.number_of_nonisomorphic_trees(-1)
    with pytest.raises(ValueError, match="order must be non-negative"):
        next(nx.nonisomorphic_trees(-1))

