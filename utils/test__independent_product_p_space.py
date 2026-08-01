
def test_IndependentProductPSpace():
    X = Normal('X', 0, 1)
    Y = Normal('Y', 0, 1)
    px = X.pspace
    py = Y.pspace
    assert pspace(X + Y) == IndependentProductPSpace(px, py)
    assert pspace(X + Y) == IndependentProductPSpace(py, px)

