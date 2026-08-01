
def test_nonisomorphic_tree_low_order_agreement(n):
    """Ensure all the order<2 'special cases' are consistent."""
    assert len(list(nx.nonisomorphic_trees(n))) == nx.number_of_nonisomorphic_trees(n)

