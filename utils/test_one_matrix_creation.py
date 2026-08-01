
def test_one_matrix_creation():
    assert OneMatrix(2, 2)
    assert OneMatrix(0, 0)
    assert Eq(OneMatrix(1, 1), Identity(1))
    raises(ValueError, lambda: OneMatrix(-1, 2))
    raises(ValueError, lambda: OneMatrix(2.0, 2))
    raises(ValueError, lambda: OneMatrix(2j, 2))
    raises(ValueError, lambda: OneMatrix(2, -1))
    raises(ValueError, lambda: OneMatrix(2, 2.0))
    raises(ValueError, lambda: OneMatrix(2, 2j))

    n = symbols('n')
    assert OneMatrix(n, n)
    n = symbols('n', integer=False)
    raises(ValueError, lambda: OneMatrix(n, n))
    n = symbols('n', negative=True)
    raises(ValueError, lambda: OneMatrix(n, n))

