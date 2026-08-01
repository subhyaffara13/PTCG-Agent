
def test_matrix_element_sets():
    X = MatrixSymbol('X', 4, 4)
    assert ask(Q.real(X[1, 2]), Q.real_elements(X))
    assert ask(Q.integer(X[1, 2]), Q.integer_elements(X))
    assert ask(Q.complex(X[1, 2]), Q.complex_elements(X))
    assert ask(Q.integer_elements(Identity(3)))
    assert ask(Q.integer_elements(ZeroMatrix(3, 3)))
    assert ask(Q.integer_elements(OneMatrix(3, 3)))
    from sympy.matrices.expressions.fourier import DFT
    assert ask(Q.complex_elements(DFT(3)))

