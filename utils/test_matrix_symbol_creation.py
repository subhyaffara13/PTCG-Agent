
def test_matrix_symbol_creation():
    assert MatrixSymbol('A', 2, 2)
    assert MatrixSymbol('A', 0, 0)
    raises(ValueError, lambda: MatrixSymbol('A', -1, 2))
    raises(ValueError, lambda: MatrixSymbol('A', 2.0, 2))
    raises(ValueError, lambda: MatrixSymbol('A', 2j, 2))
    raises(ValueError, lambda: MatrixSymbol('A', 2, -1))
    raises(ValueError, lambda: MatrixSymbol('A', 2, 2.0))
    raises(ValueError, lambda: MatrixSymbol('A', 2, 2j))

    n = symbols('n')
    assert MatrixSymbol('A', n, n)
    n = symbols('n', integer=False)
    raises(ValueError, lambda: MatrixSymbol('A', n, n))
    n = symbols('n', negative=True)
    raises(ValueError, lambda: MatrixSymbol('A', n, n))

