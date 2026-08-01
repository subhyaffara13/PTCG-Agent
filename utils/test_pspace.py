
def test_pspace():
    X, Y = Normal('X', 0, 1), Normal('Y', 0, 1)
    x = Symbol('x')

    raises(ValueError, lambda: pspace(5 + 3))
    raises(ValueError, lambda: pspace(x < 1))
    assert pspace(X) == X.pspace
    assert pspace(2*X + 1) == X.pspace
    assert pspace(2*X + Y) == IndependentProductPSpace(Y.pspace, X.pspace)

