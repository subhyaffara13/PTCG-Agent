
def test_RandomSymbol():

    X = Normal('x', 0, 1)
    Y = Normal('x', 0, 2)
    assert X.symbol == Y.symbol
    assert X != Y

    assert X.name == X.symbol.name

    X = Normal('lambda', 0, 1) # make sure we can use protected terms
    X = Normal('Lambda', 0, 1) # make sure we can use SymPy terms

