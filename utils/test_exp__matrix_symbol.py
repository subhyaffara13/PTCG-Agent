
def test_exp_MatrixSymbol():
    A = MatrixSymbol("A", 2, 2)
    assert exp(A).has(exp)

