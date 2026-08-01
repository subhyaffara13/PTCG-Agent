
def test_identity_matrix_creation():
    assert Identity(2)
    assert Identity(0)
    raises(ValueError, lambda: Identity(-1))
    raises(ValueError, lambda: Identity(2.0))
    raises(ValueError, lambda: Identity(2j))

    n = symbols('n')
    assert Identity(n)
    n = symbols('n', integer=False)
    raises(ValueError, lambda: Identity(n))
    n = symbols('n', negative=True)
    raises(ValueError, lambda: Identity(n))

