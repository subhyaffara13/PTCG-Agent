
def test_GaussianEnsemble():
    G = GaussianEnsemble('G', 3)
    assert density(G) == G.pspace.model
    raises(ValueError, lambda: GaussianEnsemble('G', 3.5))

