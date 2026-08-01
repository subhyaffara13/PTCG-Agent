
def test_unhandled_queries():
    X = MatrixSymbol("X", 2, 2)
    assert ask(Q.lt(X, 2) & Q.gt(X, 3)) is None

