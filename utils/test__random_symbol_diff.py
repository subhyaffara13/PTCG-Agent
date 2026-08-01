
def test_RandomSymbol_diff():
    X = Normal('x', 0, 1)
    assert (2*X).diff(X)

