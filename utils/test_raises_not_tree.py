
def test_raises_not_tree(fn, gen):
    """Check that broadcast functions properly raise for nontree graphs."""
    G = gen(5)
    with pytest.raises(nx.NotATree, match=r"not a tree"):
        fn(G)

