
def test_node_compare(xp):
    np.random.seed(23)
    nobs = 50
    X = np.random.randn(nobs, 4)
    Z = xp.asarray(ward(X))
    tree = to_tree(Z)
    assert_(tree > tree.get_left())
    assert_(tree.get_right() > tree.get_left())
    assert_(tree.get_right() == tree.get_right())
    assert_(tree.get_right() != tree.get_left())

